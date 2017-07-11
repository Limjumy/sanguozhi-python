#!/usr/bin/python
# encoding:utf-8
import codecs
w=['']
with codecs.open("lianxi.txt", "a+", "utf-8") as f:
    for i in range(0, 10):
        f.write(u"-------这里输出第")
        f.write(str(i))
        f.write(u"类文本的词语tf-idf权重------")

with codecs.open("lianxi.txt", "a+", "utf-8") as f:
    for i in range(93):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        f.write(u"-------这里输出第")
        f.write(str(i+1))
        f.write(u"类文本的词语tf-idf权重------")
        f.write('\r\n')