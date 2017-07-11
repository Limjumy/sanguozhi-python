#!/usr/bin/python
# encoding:utf-8
import codecs

#NO
#读取bianhao_review3.txt 三国志 书评 编号
bianhao=""
with codecs.open("1025998.txt", "r", "utf-8") as f:
    for line in f.readlines():
        bianhao=bianhao+line
    print(bianhao)