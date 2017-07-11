#!/usr/bin/python
# encoding:utf-8
import codecs

with codecs.open('sanguo(wenyanwen)_split.txt', 'r', 'utf-8') as f:
    count=0
    for line in f.readlines():
        count+=1
        print(line)
        print(type(line))
    print(count)
