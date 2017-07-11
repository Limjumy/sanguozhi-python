#!/usr/bin/python
# encoding:utf-8
import os
import codecs
import re
import jieba
from gensim import corpora, models, similarities

from gensim.corpora import Dictionary
from gensim.models import LdaModel

#为去除停用词
stopwords=[line.strip().decode('utf-8') for line in open('stopwords.txt','rb').readlines()]

#jieba.load_userdict("sanguozhi.scel")
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
    review=eachFile(filePath,review)
    for line in review: # 将93条评论读入了review中
        print(line)
        print(type(line)) #问题就在于这里的line是列表形式
        jiebas=jieba.cut(line,cut_all=False) # cut_all=False是精确模式，不是全模式
        words.append(list(set(jiebas)-set(stopwords)-set(' '))) # 去除停用词
    print(words)
    #print(len(review)) # 93


    #得到的分词结果构造词典
    dictionary = corpora.Dictionary(words)
    print(dictionary)
    print(dictionary.token2id)

    #为了方便看，我给了个循环输出：

    for word, index in dictionary.token2id.items():
        print(word + " 编号为:" + str(index))


    # 词典生成好之后，就开始生成语料库了
    corpus = [dictionary.doc2bow(text) for text in words]
    print(corpus)


    # lda模型训练
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=9)

    for i in range(9):
        print(lda.print_topics(i))
        print(type(lda.print_topics(i)))

    # 将计算好的主题模型写到文件中
    sim_file = open("Lda_sanguozhi_.txt", 'w')
    for i in range(9):
        for line in lda.print_topics(i):
            print(lda.print_topics(i))
            #for w in line:
            #    sim_file.write(w)
    sim_file.close()














