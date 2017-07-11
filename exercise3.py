#!/usr/bin/python
# encoding:utf-8
import codecs

with codecs.open("shiyan_result.txt", "a+", "utf-8") as f:
    f.write('new para ')
    f.write('\r\n')####换行终于成功了！！1试了很多次'\n'都不行
    f.write('sssss')