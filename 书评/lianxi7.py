#!/usr/bin/python
# encoding:utf-8
import os
import codecs
import jieba
import re
import jieba.posseg as pseg
from gensim import corpora, models, similarities
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
import numpy as np
import matplotlib.pylab as plt
from sklearn.cluster import KMeans

jieba.load_userdict("names_sanguoyy.txt")  # 加载字典
jieba.load_userdict("names_sanguo.txt")
jieba.load_userdict("review_cidian.txt")

def bianli_fenci(filepath,list):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir: #对于每一篇评论，每一篇评论是列表list的一个元素
        child = os.path.join('%s%s' % (filepath, allDir))
        print(child) # 遍历了目录下的一个个文件名字
        cotent_child=""
        # 读取文件child
        with codecs.open(child, "r", "utf-8") as f:
            for line in f.readlines():
                cotent_child = cotent_child + line
                #print(type(cotent_child)) #str
                # 去掉评论中的各中html格式
            cotent_child=re.sub("[\.\!\/_,$%^*(+\"\'\\r]+|[+——！，。？?、~@#￥%……&*（）<>\\n]+|[div]+|[p]+|[nbs;]+|[br]+|[h2]+]", "",cotent_child)
            list.append(cotent_child) #将这一评论的内容(字符串)加入列表，作为列表的元素之一
        #list=readFile(child,list)
    return list





if __name__ == '__main__':
    review=[]
    roles_review = []
    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=bianli_fenci(filePath,review) # review的格式为['','','','']
    for line in review: # 将93条评论读入了review中,一条是一个元素
        roles_review.append([])
        #print(line)
        #print(type(line)) #问题就在于这里的line是列表形式，现在是str
        poss = pseg.cut(line)  # 分词并返回该词词性
        for w in poss:
            if w.flag != 'na':
                continue
            roles_review[-1].append(w.word)
    # roles_review去重写入
    for line in roles_review:# roles_review的格式为[['',''],['','']]
        # new_roles_review=list(set(line))# 去重 乱序
        #去重 正序
        new_roles_review = []
        for li in line:  # line格式为['','']
            if li not in new_roles_review:
                new_roles_review.append(li)
        #print(new_roles_review)
        print(len(new_roles_review)) # new_roles_review的格式为['','']