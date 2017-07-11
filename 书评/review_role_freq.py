#!/usr/bin/python
# encoding:utf-8

# 计算每篇评论中出现的人物词频
import os
import re
import codecs
import jieba.posseg as pseg
import jieba

jieba.load_userdict("names_sanguoyy.txt")  # 加载字典
jieba.load_userdict("names_sanguo.txt")
jieba.load_userdict("review_cidian.txt")
def eachFile(filepath,lineNames):
    #lineNames=[]
    pathDir =  os.listdir(filepath)
    for allDir in pathDir: #对于每一篇评论，每一篇评论是列表list的一个元素
        child = os.path.join('%s%s' % (filepath, allDir))
        #print (child.decode('gbk')) # .decode('gbk')是解决中文显示乱码问题
        print(child) # 遍历了目录下的一个个文件名字
        cotent_child=""
        # 读取文件child
        with codecs.open(child, "r", "utf-8") as f:
            names={}
            for line in f.readlines():
                cotent_child = cotent_child + line #每篇评论的内容
            # 去掉评论中的各种英文
            cotent_child=re.sub("[\.\!\/_,$%^*(+\"\'\\r]+|[+——！，。？?、~@#￥%……&*（）<>\\n]+|[A-Za-z]+", "",cotent_child)
            # 对评论分词，并筛选人物
            poss = pseg.cut(cotent_child)  # 分词并返回该词词性
            lineNames.append([])  # 为新读入的一段添加人物名称列表
            for w in poss:
                if w.flag != "na" :
                    continue  # 当分词长度小于2或该词词性不为nr时认为该词不为人名
                if names.get(w.word) is None:
                    names[w.word] = 0
                names[w.word] += 1  # 该人物出现次数加 1
            lineNames[-1].append(names)  # 为当前段的环境增加一个人物
            #list.append(cotent_child) #将这一评论的内容加入列表，作为列表的元素之一
    return lineNames

def write_listline(filename,lineNames):
    with codecs.open(filename, "a+", "utf-8") as f:
        counts=0
        for line in lineNames: #line的格式为['','']
            counts+=1
            f.write("这是第")
            f.write(str(counts))
            f.write("篇评论"+"     ")
            #print(line)
            for line_ in line: # line_是字典
                f.write(str(len(line_)))
                f.write("个人物")
                f.write('\r\n')
                print(len(line_))
                for name, times in line_.items():
                    f.write(name + " " + str(times) + "\r\n")


if __name__ == '__main__':
    review=[]
    words = []
    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=eachFile(filePath,review) # review的格式为['','','','']
    filename="review_mainroles_each.txt"
    write_listline(filename,review)
