from zheye import zheye


from zheye import zheye
z = zheye()
positions = z.Recognize('/Users/chris/Pyproject/scrapy/Articlespider/b.gif')
positions.sort(key=lambda x:x[1])
print(positions)
