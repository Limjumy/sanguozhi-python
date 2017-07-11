#!/usr/bin/python
# encoding:utf-8
import jieba
import os
import codecs
import re
from gensim import corpora, models, similarities
import jieba.posseg as pseg

jieba.load_userdict("names_sanguoyy.txt")  # 加载字典
jieba.load_userdict("names_sanguo.txt")
jieba.load_userdict("review_cidian.txt")

# 遍历评论文本，只筛选人名，来看评论间的相似性

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

# 将人物变为词典试试
    # 得到的分词结果构造词典
    dictionary = corpora.Dictionary(roles_review)
    print(dictionary)
    print(dictionary.token2id)

    # 输出词典中的词语编号
    for word, index in dictionary.token2id.items():
        print(word + " 编号为:" + str(index))

# 将每篇书评用向量表示，聚类
    corpus = [dictionary.doc2bow(text) for text in roles_review]
    print(corpus)
    #print(corpus)corpus格式为[[(0,2),(1,2)],[(),()]] 成功

    # 将元组数据 调整表示成 词向量（词语为行按编号，词频为列，一行表示一个评论）
    # 将[(0,2),(1,2)]变为[2,2,0,0,0,0,0,0,0....]
    #corpus = [[(1, 2), (3, 4)], [(4, 2)]]
    yuanzu2list = []
    for line in corpus:  # [(0,2),(1,2)]
        yuanzu2list.append([])
        for i in range(478):
            yuanzu2list[-1].append(0)
        if len(line) == 0:
            continue
        for yuanzu in line:
            yuanzu2list[-1][yuanzu[0]] = yuanzu[1]
    print(yuanzu2list)

    # 写入
    with codecs.open("role_freq.txt", "a+", "utf-8") as f:
        for line in yuanzu2list:
            for shuzi in line:
                f.write(str(shuzi))
                f.write(' ')
            f.write('\n')