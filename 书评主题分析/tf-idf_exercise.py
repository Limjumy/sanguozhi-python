#!/usr/bin/python
# encoding:utf-8
import os
import codecs
import re
import jieba
from gensim import corpora, models, similarities


# 呈现评论之间的相似性
# 将评论表示为向量


jieba.load_userdict("pl_cidian.txt")  # 加载字典
#为去除停用词
stopwords=[line.strip().decode('utf-8') for line in open('stopwords.txt','rb').readlines()]



# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath,list):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir: #对于每一篇评论，每一篇评论是列表list的一个元素
        child = os.path.join('%s%s' % (filepath, allDir))
        #print (child.decode('gbk')) # .decode('gbk')是解决中文显示乱码问题
        print(child) # 遍历了目录下的一个个文件名字
        cotent_child=""
        # 读取文件child
        with codecs.open(child, "r", "utf-8") as f:
            for line in f.readlines():
                cotent_child = cotent_child + line
                # 去掉评论中的各种英文
            cotent_child=re.sub("[\.\!\/_,$%^*(+\"\'\\r]+|[+——！，。？?、~@#￥%……&*（）<>\\n]+|[A-Za-z]+", "",cotent_child)
            list.append(cotent_child) #将这一评论的内容加入列表，作为列表的元素之一
        #list=readFile(child,list)
    return list

if __name__ == '__main__':
    review=[]
    words = []
    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=eachFile(filePath,review)
    for line in review: # 将93条评论读入了review中
        print(line)
        print(type(line)) #问题就在于这里的line是列表形式
        jiebas = jieba.cut(line, cut_all=False)  # cut_all=False是精确模式，不是全模式
        words.append(list(set(jiebas) - set(stopwords)-set(' ')))  # 去除停用词
    print(words)


