#!/usr/bin/python
# encoding:utf-8
import os
import codecs
import jieba
import re
import jieba.posseg as pseg
from gensim import corpora, models, similarities
# 注意此处documents格式
documents = ["曹操 裴松之 恩恩 小酒 小酒 曹操 刘备",
                                               "龙门 孔明 貂蝉 小酒 曹操 刘备",
                                               "大乔 拿破仑 孔明"]
#Vectorizer = StemmedCountVectorizer
#vectorizer.fit_transform(documents)
#texts = vectorizer.get_feature_names()

dictionary = corpora.Dictionary(documents)   # 生成词典
for word, index in dictionary.token2id.items():
    print(word + " 编号为:" + str(index))
# print(texts)

corpus = [dictionary.doc2bow(text) for text in documents]
print(corpus)

