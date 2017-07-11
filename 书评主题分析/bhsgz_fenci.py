#!/usr/bin/python
# encoding:utf-8
import codecs
import jieba
import jieba.posseg as pseg

## 未完成！！
# 将白话三国志分词处理下，作为“商品描述”
list=[]
with codecs.open('E:\\python_project\\三国志\\bhsgz.txt', "r","utf-8") as f:
    for line in f.readlines():
        # query=q_file.readline()
        #list.append(list(jieba.cut(line)))
        poss = pseg.cut(line)  # 分词并返回该词词性
        list.append(poss)
    print(list)