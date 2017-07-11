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
def readFile(filename,list):
    fopen = open(filename, 'r') # r 代表read
    for eachLine in fopen:
        list[-1].append(eachLine) # 返回列表
        #print ("读取到得内容如下：",eachLine) # 打印
    fopen.close()

# LDA模型
def lsi_similar(corpus_tfidf,query):
    lda=models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=5)
    #lsi.print_topics(5)
    corpus_lsi = lda[corpus_tfidf]
    index=similarities.MatrixSimilarity(lda[corpus])
    #query="曹操 诸葛亮 刘备"
    query_bow=dictionary.doc2bow(query.lower().split())
    # 训练好的LSI模型将其映射到二维的topic空间
    query_lda = lda[query_bow]
    # 计算其和index中doc的余弦相似度
    sims=index[query_lda]
    # 按相似度进行排序
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return (sort_sims)
    #return list(enumerate(sims))




def lda_plot(corpus):
    ## 做聚类试试，结果不好
    import numpy as np
    import matplotlib.pylab as plt
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=5, alpha=5)
    corpus_lda = lda[corpus_tfidf]

    # # 画图
    thetas = [lda[c] for c in corpus_tfidf]
    plt.hist([len(t) for t in thetas], np.arange(10))
    plt.ylabel('Nr of reviews')
    plt.xlabel('Nr of topics')
    plt.show()
    return corpus_lda

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

if __name__ == '__main__':
    review=[]
    words = []
    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=eachFile(filePath,review) # review的格式为['','','','']
    for line in review: # 将93条评论读入了review中
        print(line)
        #print(type(line)) #问题就在于这里的line是列表形式，现在是str
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

    # LSI模型
    #query='天涯 明月 望断 哀叹'
    # 将《三国志》分词作为query
    #query='情意 思绪 阳光 照射 柳絮 紫月 含情 杨柳 秋水 白雪 寒蝉凄切 悲剧 断续残阳 相思 血泪 沧海 离愁 春水 愁 哀叹 朝存夕亡 无尽 春来 脉脉 明月 天涯 断肠人 风霜 哀叹 追忆 残垣断壁 皑皑白骨 白发'
    #query='阳光 照射 断续残阳 残垣断壁 皑皑白骨 杨柳 白雪 悲剧 哀叹 梦 海上生明月 那一刻 泪流满面 港湾 画面 终归 沉浮 青丝 顾盼'
    query=''
    with codecs.open('shop_describe_split.txt', 'r','utf-8') as f:
        for line in f.readlines():
           #print(line)
            query=query+' '+line
    #print(query)
    print(len(query))
    lsi_list=lsi_similar(corpus_tfidf, query)
    #with codecs.open('sanguo_similar.txt', 'a+', 'utf-8') as f:
    for line in lsi_list[0:93]:
        print(line)
            #f.write(line)
            #f.write('\n')

    #for line in words[40]:
    #    print(line)








