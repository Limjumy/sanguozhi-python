#!/usr/bin/python
# encoding:utf-8
from gensim import corpora, models, similarities
import jieba

sentences = ["我喜欢吃土豆","土豆是个百搭的东西","我不喜欢今天雾霾的北京"]

words=[]
for doc in sentences:
    words.append(list(jieba.cut(doc)))
print (words)

# 得到的分词结果构造词典

dic = corpora.Dictionary(words)
print (dic)
print (dic.token2id)

#为了方便看，我给了个循环输出：
for word,index in dic.token2id.items():
    print (word +" 编号为:"+ str(index))


# 词典生成好之后，就开始生成语料库了
corpus = [dic.doc2bow(text) for text in words]
print("语料 "+corpus)

# 得到了语料库，接下来做一个TF-IDF变换
tfidf = models.TfidfModel(corpus)
vec = [(0, 1), (4, 1)]
print(tfidf[vec])
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)

#vec是查询文本向量，比较vec和训练中的三句话相似度
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=14)
sims = index[tfidf[vec]]
print (list(enumerate(sims)))

# 回到tfidf转换，接着训练LSI模型，假定三句话属于2个主题，
lsi = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=2)
lsiout=lsi.print_topics(2)
print (lsiout[0])
print (lsiout[1])

# 将文章投影到主题空间中
corpus_lsi = lsi[corpus_tfidf]
for doc in corpus_lsi:
    print (doc)




