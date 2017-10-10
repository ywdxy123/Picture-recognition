def resize(self, maxwidth=1000, maxheight=1000):
        """
        基于最大宽高按比例重设图片大小，
        注意：这可能影响检测算法的结果

        如果没有变化返回 0
        原宽度大于 maxwidth 返回 1
        原高度大于 maxheight 返回 2
        原宽高大于 maxwidth, maxheight 返回 3

        maxwidth - 图片最大宽度
        maxheight - 图片最大高度
        传递参数时都可以设置为 False 来忽略
        """
        # 存储返回值
        ret = 0
        if maxwidth:
            if self.width > maxwidth:
                wpercent = (maxwidth / self.width)
                hsize = int((self.height * wpercent))
                fname = self.image.filename
                # Image.LANCZOS 是重采样滤波器，用于抗锯齿
                self.image = self.image.resize((maxwidth, hsize), Image.LANCZOS)
                self.image.filename = fname
                self.width, self.height = self.image.size
                self.total_pixels = self.width * self.height
                ret += 1
        if maxheight:
            if self.height > maxheight:
                hpercent = (maxheight / float(self.height))
                wsize = int((float(self.width) * float(hpercent)))
                fname = self.image.filename
                self.image = self.image.resize((wsize, maxheight), Image.LANCZOS)
                self.image.filename = fname
                self.width, self.height = self.image.size
                self.total_pixels = self.width * self.height
                ret += 2
        return ret
