#!/usr/bin/python
# encoding:utf-8
list=[[]]

filename = "E:\\python_project\\爬虫\\长评论\\1025998.txt"

fopen = open(filename, 'r') # r 代表read
for eachLine in fopen:
    list[-1].append(eachLine) # 返回列表
