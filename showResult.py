# 将在源文件目录生成图片文件，将皮肤区域可视化
def showSkinRegions(self):
    # 未得出结果时方法返回
    if self.result is None:
        return
    # 皮肤像素的 ID 的集合
    skinIdSet = set()
    # 将原图做一份拷贝
    simage = self.image
    # 加载数据
    simageData = simage.load()
    
    # 将皮肤像素的 id 存入 skinIdSet
    for sr in self.skin_regions:
        for pixel in sr:
            skinIdSet.add(pixel.id)
    # 将图像中的皮肤像素设为白色，其余设为黑色
    for pixel in self.skin_map:
        if pixel.id not in skinIdSet:
            simageData[pixel.x, pixel.y] = 0, 0, 0
        else:
            simageData[pixel.x, pixel.y] = 255, 255, 255
    # 源文件绝对路径
    filePath = os.path.abspath(self.image.filename)
    # 源文件所在目录
    fileDirectory = os.path.dirname(filePath) + '/'
    # 源文件的完整文件名
    fileFullName = os.path.basename(filePath)
    # 分离源文件的完整文件名得到文件名和扩展名
    fileName, fileExtName = os.path.splitext(fileFullName)
    # 保存图片
    simage.save('{}{}_{}{}'.format(fileDirectory, fileName,'Nude' if self.result else 'Normal', fileExtName))
