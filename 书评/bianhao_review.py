#!/usr/bin/python
# encoding:utf-8

import os
import codecs


##遍历filePath下的所有txt文件
# 读取txt文件的第一行 为列表
# 统计每条评论的字数（
# 统计每条评论的关键词（根据人名可以试试）
def bianli_docuname(filepath,list):
    pathDir = os.listdir(filepath)
    for allDir in pathDir:  # 对于每一篇评论，每一篇评论是列表list的一个元素
        child = os.path.join('%s%s' % (filepath, allDir))
        print(child)  # 遍历了目录下的一个个文件名字
        # 读取文件child

        with codecs.open(child, "r", "utf-8") as f:
            counts = 0
            for line in f.readlines():
                if counts==0: # 只读第一行
                    counts=counts+1
                    list.append(line)
                else:
                    continue
                # print(type(cotent_child)) #str
                # 去掉评论中的各种符号，此处
            # cotent_child=re.sub("[\.\!\/_,$%^*(+\"\'\\r]+|[+——！，。？?、~@#￥%……&*（）<>\\n]+|[A-Za-z]+", "",cotent_child)
    return list

if __name__ == '__main__':
    review_biaoti=[]

    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=bianli_docuname(filePath,review_biaoti)
    for line in review_biaoti: # 将93条评论标题读入了review中
        print(line)
        print(type(line)) #问题就在于这里的line是列表形式

# 将评论编号写入csv
# 将评论标题希尔同一个csv
    bianhao=[]
    with codecs.open("bianhao.txt", "r") as f:
        for line in f.readlines():
            bianhao.append(line)
# 此处要将编号排个序，因为读取长评论文件夹时，文件夹的顺序是正的。

# 写入
    with codecs.open("reviews_biaoti.txt", "a+","utf-8") as f:
        for line in review_biaoti:
            f.write(line)