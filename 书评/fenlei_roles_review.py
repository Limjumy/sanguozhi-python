#!/usr/bin/python
# encoding:utf-8

# 对书评遍历
# 对每个书评分词，提取其中人名,写入文件fenlei_roles_review2.txt，是正序
# 用gensim包，生成词典
# 将文档变成词典 参考lianxi2.py
# #LSI模型——搜索最相似
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

def tfidf_plot(corpus):
    ## 画图
    import matplotlib.pylab as plt
    # # 聚类效果不好，
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    #print('corpus_tfidf')
    #print(corpus_tfidf)

    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=5)
    #print('lda_print_topic')
    #lda.print_topics(5)
    #corpus_lda = lda[corpus_tfidf]
    thetas = [lda[c] for c in corpus_tfidf]
    plt.hist([len(t) for t in thetas], np.arange(100))
    plt.ylabel('Nr of reviews')
    plt.xlabel('Nr of topics')
    plt.show()

# LSI模型
def lsi_similar(corpus_tfidf,query):
    lsi=models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=5)
    lsi.print_topics(5)
    corpus_lsi = lsi[corpus_tfidf]
    index=similarities.MatrixSimilarity(lsi[corpus])
    #query="曹操 诸葛亮 刘备"
    query_bow=dictionary.doc2bow(query.lower().split())
    # 训练好的LSI模型将其映射到二维的topic空间
    query_lsi = lsi[query_bow]
    # 计算其和index中doc的余弦相似度
    sims=index[query_lsi]
    # 按相似度进行排序
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return (sort_sims)
    #return list(enumerate(sims))



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
        # 写入
        #with codecs.open("fenlei_roles_review2.txt", "a+", "utf-8") as f:
        #    for ss in new_roles_review:
        #        f.write(ss)
        #        f.write(' ')
        #    f.write('\r\n')


    # 将人物变为词典试试
    # 得到的分词结果构造词典
    dictionary = corpora.Dictionary(roles_review)
    print(dictionary)
    print(dictionary.token2id)

    # 输出词典中的词语编号
    #for word, index in dictionary.token2id.items():
    #    print(word + " 编号为:" + str(index))

    # 将每篇书评用向量表示，聚类
    corpus = [dictionary.doc2bow(text) for text in roles_review]
    #print(corpus)corpus格式为[[(0,2),(1,2)],[(),()]] 成功


    ##LSI模型——搜索最相似
    query = "曹操 诸葛亮 刘备"
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi_list=lsi_similar(corpus_tfidf,query)
    print(lsi_list[0:3])# 打印前三个最相似


    # 元组的写入txt
    #file="review_vectors.txt"
    #yuanzu_write(corpus,file)

## 进行层次聚类，对corpus的元素
    # 1. 层次聚类
    #生成点与点之间的距离矩阵,这里用的欧氏距离:
    #disMat = sch.distance.pdist(corpus, 'euclidean')
    #进行层次聚类:
    #Z = sch.linkage(disMat, method='average')
    #将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
    #P = sch.dendrogram(Z)
    #plt.savefig('plot_dendrogram.png')
    #根据linkage matrix Z得到聚类结果:
    #cluster = sch.fcluster(Z, t=1, 'inconsistent')

# 进行k-means聚类,需要将向量转化成k-means要求的格式(array)


    #num_clusters = 5
    #km = KMeans(n_clusters=num_clusters)
    #% time
    #km.fit(corpus)
    #clusters = km.labels_.tolist()
    #print(clusters)

    ## 聚类效果不好，
    #tfidf = models.TfidfModel(corpus)
    #corpus_tfidf = tfidf[corpus]
    #print('corpus_tfidf')
    #print(corpus_tfidf)

    #lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=5)
    #print('lda_print_topic')
    #lda.print_topics(5)
    #corpus_lda = lda[corpus_tfidf]






