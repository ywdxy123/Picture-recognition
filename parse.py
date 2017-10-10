def parse(self):
    # 如果已有结果，返回本对象
    if self.result is not None:
        return self
    # 获得图片所有像素数据
    pixels = self.image.load()
    # 遍历每个像素
    for y in range(self.height):
        for x in range(self.width):
            # 得到像素的 RGB 三个通道的值
            # [x, y] 是 [(x,y)] 的简便写法
            r = pixels[x, y][0]   # red
            g = pixels[x, y][1]   # green
            b = pixels[x, y][2]   # blue
            # 判断当前像素是否为肤色像素
            isSkin = True if self._classify_skin(r, g, b) else False
            # 给每个像素分配唯一 id 值（1, 2, 3...height*width）
            # 注意 x, y 的值从零开始
            _id = x + y * self.width + 1
            # 为每个像素创建一个对应的 Skin 对象，并添加到 self.skin_map 中
            self.skin_map.append(self.Skin(_id, isSkin, None, x, y))
            # 若当前像素不为肤色像素，跳过此次循环
            if not isSkin:
                continue
            # 设左上角为原点，相邻像素为符号 *，当前像素为符号 ^，那么相互位置关系通常如下图
            # ***
            # *^
            # 存有相邻像素索引的列表，存放顺序为由大到小，顺序改变有影响
            # 注意 _id 是从 1 开始的，对应的索引则是 _id-1
            check_indexes = [_id - 2, # 当前像素左方的像素
                              _id - self.width - 2,  # 当前像素左上方的像素
                              _id - self.width - 1,  # 当前像素的上方的像素
                             _id - self.width]  # 当前像素右上方的像素
            # 用来记录相邻像素中肤色像素所在的区域号，初始化为 -1
            region = -1
            # 遍历每一个相邻像素的索引
            for index in check_indexes:
                # 尝试索引相邻像素的 Skin 对象，没有则跳出循环
                try:
                    self.skin_map[index]
                except IndexError:
                    break
                # 相邻像素若为肤色像素：
                if self.skin_map[index].skin:
                    # 若相邻像素与当前像素的 region 均为有效值，且二者不同，且尚未添加相同的合并任务
                    if (self.skin_map[index].region != None and
                            region != None and region != -1 and
                        self.skin_map[index].region != region and
                            self.last_from != region and
                            self.last_to != self.skin_map[index].region) :
                        # 那么这添加这两个区域的合并任务
                        self._add_merge(region, self.skin_map[index].region)
                    # 记录此相邻像素所在的区域号
                    region = self.skin_map[index].region
                    # 遍历完所有相邻像素后，若 region 仍等于 -1，说明所有相邻像素都不是肤色像素
            if region == -1:
                # 更改属性为新的区域号，注意元祖是不可变类型，不能直接更改属性
                _skin = self.skin_map[_id - 1]._replace(region=len(self.detected_regions))
                self.skin_map[_id - 1] = _skin
                # 将此肤色像素所在区域创建为新区域
                self.detected_regions.append([self.skin_map[_id - 1]])
                # region 不等于 -1 的同时不等于 None，说明有区域号为有效值的相邻肤色像素
            elif region != None:
                # 将此像素的区域号更改为与相邻像素相同
                _skin = self.skin_map[_id - 1]._replace(region=region)
                self.skin_map[_id - 1] = _skin
                # 向这个区域的像素列表中添加此像素
                self.detected_regions[region].append(self.skin_map[_id - 1])
    # 完成所有区域合并任务，合并整理后的区域存储到 self.skin_regions
    self._merge(self.detected_regions, self.merge_regions)
    # 分析皮肤区域，得到判定结果
    self._analyse_regions()
    return self
# self.merge_regions 的元素都是包含一些 int 对象（区域号）的列表
# self.merge_regions 的元素中的区域号代表的区域都是待合并的区域
# 这个方法便是将两个待合并的区域号添加到 self.merge_regions 中
