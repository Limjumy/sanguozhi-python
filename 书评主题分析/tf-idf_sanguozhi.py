#!/usr/bin/python
# encoding:utf-8
import os
import codecs
import re
import jieba
from gensim import corpora, models, similarities

jieba.load_userdict("names_sanguoyy.txt")  # 加载字典
jieba.load_userdict("names_sanguo.txt")
jieba.load_userdict("review_cidian.txt")
#为去除停用词
stopwords=[line.strip().decode('utf-8') for line in open('stopwords.txt','rb').readlines()]
#line = line.decode("utf8")
 #     string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),line)
# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath,list):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir: #对于每一篇评论，每一篇评论是列表list的一个元素
        child = os.path.join('%s%s' % (filepath, allDir))
        #print (child.decode('gbk')) # .decode('gbk')是解决中文显示乱码问题
        print(child) # 遍历了目录下的一个个文件名字
        cotent_child=""
        # 读取文件child
        with codecs.open(child, "r", "utf-8") as f:
            for line in f.readlines():
                cotent_child = cotent_child + line
                #print(type(cotent_child)) #str
                # 去掉评论中的各种英文
            cotent_child=re.sub("[\.\!\/_,$%^*(+\"\'\\r]+|[+——！，。？?、~@#￥%……&*（）<>\\n]+|[A-Za-z]+", "",cotent_child)
            list.append(cotent_child) #将这一评论的内容加入列表，作为列表的元素之一
        #list=readFile(child,list)
    return list


# 读取文件内容并（打印）写入列表
#def readFile(filename,list):
#    fopen = open(filename, 'r') # r 代表read
#    for eachLine in fopen:
#        list[-1].append(eachLine) # 返回列表
 #       #print ("读取到得内容如下：",eachLine) # 打印
  #  fopen.close()



if __name__ == '__main__':
    review=[]
    words = []
    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=eachFile(filePath,review) # review的格式为['','','','']
    for line in review: # 将93条评论读入了review中
        print(line)
        print(type(line)) #问题就在于这里的line是列表形式，现在是str
        jiebas = jieba.cut(line, cut_all=False)  # cut_all=False是精确模式，不是全模式
        words.append(list(set(jiebas) - set(stopwords)))  # 去除停用词
    print(words)
    #print(len(review)) # 93


    #得到的分词结果构造词典
    dictionary = corpora.Dictionary(words)
    print(dictionary)
    print(dictionary.token2id)

    #为了方便看，我给了个循环输出：

    #for word, index in dictionary.token2id.items():
    #    print(word + " 编号为:" + str(index))


    # 词典生成好之后，就开始生成语料库了
    corpus = [dictionary.doc2bow(text) for text in words]
    print(corpus)

    # 得到了语料库，接下来做一个TF-IDF变换
    tfidf = models.TfidfModel(corpus)
    # 此处已经得到所有评论的tf-idf值
    corpus_tfidf = tfidf[corpus]
    #for doc in corpus_tfidf: #最好能够输出写入文档！！！！！
    #    print(doc)
        #file = open("tfdif.txt", 'w')
        #for line in doc:
        #    file.write(line+" ")
        #file

    # 将白话三国志分词处理下，作为“商品描述”
    #q_file = open('bhsgz_split.txt', 'r')
    #query = q_file.readline()
    #q_file.close()

    # 用第一个评论试一试##############
    #query1=""
    #for line in words[0]:
    #    query1=query1+line


    # 把商品描述转成词包
    #vec_bow = dictionary.doc2bow(query.split())
    # 直接使用评论的tf-idf模型得到商品描述的tf-idf值
    #vec_tfidf = tfidf[vec_bow]

    # 把所有评论做成索引
    #index = similarities.MatrixSimilarity(corpus_tfidf)
    # 利用索引计算每一条评论和商品描述之间的相似度
    #sims = index[vec_tfidf]
    # 把相似度存储成列表，以便写入txt 文档
    #similarity = list(sims)

    # 将计算好的相似度写到文件中
    #sim_file = open("lda_sanguozhi.txt", 'w')
    #for i in similarity:
    #    sim_file.write(str(i) + '\n')
    #sim_file.close()

    ## 做聚类试试，结果不好
    import numpy as np
    import matplotlib.pylab as plt
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=3, alpha=1)
    corpus_lda = lda[corpus_tfidf]

    # # 画图
    thetas = [lda[c] for c in corpus_tfidf]
    plt.hist([len(t) for t in thetas], np.arange(10))
    plt.ylabel('Nr of reviews')
    plt.xlabel('Nr of topics')
    plt.show()
