#!/usr/bin/python
# encoding:utf-8
import os
import codecs
def bianli_fenci(filepath,child_list):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir: #对于每一篇评论，每一篇评论是列表list的一个元素
        child = os.path.join('%s%s' % (filepath, allDir))
        #print (child.decode('gbk')) # .decode('gbk')是解决中文显示乱码问题
        print(child) # 遍历了目录下的一个个文件名字
        # 读取文件child
        with codecs.open(child, "r", "utf-8") as f:
            counts=0
            for line in f.readlines():
                counts += 1
                print(counts==2)
                if counts>2:
                    continue
                if counts==2:
                    child_list.append(line)
                    print(line)
    return child_list



if __name__ == '__main__':
    review=[]
    roles_review = []
    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=bianli_fenci(filePath,review) # review的格式为['','','','']

    with codecs.open("star_qgfx.txt", "a+", "utf-8") as f:
        for line in review:
            f.write(line)