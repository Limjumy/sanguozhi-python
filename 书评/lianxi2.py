#!/usr/bin/python
# encoding:utf-8

# 试验gensim包中的词典，注意生成词典需要的list格式
# 结论：词典中的词语没有重复
# 将文档转换为向量 可直接打印
# 元组写入txt 按向量格式
import os
import codecs
import jieba
import re
import jieba.posseg as pseg
from gensim import corpora, models, similarities
# 注意此处documents格式
documents = [["曹操","裴松之","恩恩","小酒","小酒","曹操","刘备"],
                                               ["龙门","孔明","貂蝉","小酒","曹操","刘备"],
                                               ["大乔","拿破仑","孔明"]]
dictionary = corpora.Dictionary(documents)   # 生成词典
for word, index in dictionary.token2id.items():
    print(word + " 编号为:" + str(index))

# diction.token2id 存放的是单词-id key-value对
# diction.dfs 存放的是单词的出现频率
print(dictionary.dfs)
# 将文档转换为向量
corpus = [dictionary.doc2bow(text) for text in documents]
print(corpus)
print(type(corpus)) # list
#
#tfidf = models.TfidfModel(corpus)
#corpus_tfidf = tfidf[corpus]
#lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=5, alpha=3)
#corpus_lda = lda[corpus_tfidf]
#from gensim import corpora, models, matutils

#lda_csc_matrix = matutils.corpus2csc(corpus_lda).transpose()
#print(type(lda_csc_matrix))





# 聚类
## 聚类效果
import matplotlib.pylab as plt
import numpy as np
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=3, alpha=1)
corpus_lda = lda[corpus_tfidf]

# #####
topics = [lda[c] for c in corpus_tfidf]
print(topics)
####

    ## 画图
thetas = [lda[c] for c in corpus_tfidf]
plt.hist([len(t) for t in thetas], np.arange(100))
plt.ylabel('Nr of reviews')
plt.xlabel('Nr of topics')
plt.show()

# 元组的写入txt
# 写入元组
def yuanzu_write(corpus,file):
    with codecs.open(file, "a+") as f:
        for line in corpus:  # corpus的格式为[[(),()],[(),()]]  # line [(),()]
            counts = 0
            f.write('(')
            for vectors in line:  # vectors (0,2)元组
                counts += 1
                f.write('(')
                f.write(str(vectors[0]))
                f.write(',')
                f.write(str(vectors[1]))
                f.write(")")
                if counts == len(line):
                    f.write(')')
                    continue
                f.write(',')
            f.write('\n')

## 聚类
from numpy import array

import gensim
from scipy.cluster.vq import vq, kmeans, whiten
# 如何将corpus转化为要求的格式array
#numpy_matrix = gensim.matutils.corpus2dense(corpus)
#print(type(numpy_matrix))
#array_corpus=np.array(numpy_matrix)
#print(corpus)
#kmeans(array_corpus,2, iter=20, thresh=1e-05, check_finite=True)

