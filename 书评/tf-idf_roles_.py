#!/usr/bin/python
# encoding:utf-8

import os
import codecs
import jieba
import re
# 遍历每条书评，分词，留下人名na和nr
# 根据每条评论涉及的人名，根据tf-idf
# 统计每条评论的关键词（根据人名可以试试）

jieba.load_userdict("names_sanguoyy.txt")  # 加载字典
jieba.load_userdict("names_sanguo.txt")
jieba.load_userdict("review_cidian.txt")
#为去除停用词
stopwords=[line.strip().decode('utf-8') for line in open('stopwords.txt','rb').readlines()]

def bianli_fenci(filepath,list):
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
            cotent_child=re.sub("[\.\!\/_,$%^*(+\"\'\\r]+|[+——！，。？?、~@#￥%……&*（）<>\\n]+|[div]+|[p]+|[nbs;]+|[br]+|[h2]+]", "",cotent_child)
            list.append(cotent_child) #将这一评论的内容加入列表，作为列表的元素之一
        #list=readFile(child,list)
    return list

# 函数：写入txt文件
def print_tidif(file,word,weight,lis):
    with codecs.open(file, "a+", "utf-8") as f:
        for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            f.write(u"-------这里输出第")
            f.write(str(i + 1))
            f.write(u"条书评的关键词词语tf-idf权重------")
            f.write('\r\n')
            for j in range(len(word)):
                #if weight[i][j] <= 0.05:
                if weight[i][j]<=0.9:
                    continue
                lis.append(str(i+1))# 记录是第几篇评论有TD-IDF值大于0.1
                f.write(word[j])
                f.write(' ')
                f.write(str(weight[i][j]))
                f.write('\r\n')

if __name__ == '__main__':
    review=[]
    roles_review = []
    filePath = "E:\\python_project\\爬虫\长评论\\"
    review=bianli_fenci(filePath,review) # review的格式为['','','','']
    for line in review: # 将93条评论读入了review中,一条是一个元素
        roles_review.append([])
        #print(line)
        #print(type(line)) #问题就在于这里的line是列表形式，现在是str
        import jieba.posseg as pseg
        poss = pseg.cut(line)  # 分词并返回该词词性
        for w in poss:
            if w.flag != 'na':
                continue
            roles_review[-1].append(w.word)

    print(roles_review[0:2])


    # roles_review 存储了每篇书评出现的人物词语，词语由重复。因为有重复才能做TF-IDF分析
    # #!!!这里corpus需要的格式是字符串，但是是一段整个的字符串，一个文本即为一整个字符串
    # 所以，将corpus的元素变为字符串
    corpus_str = []
    for line in roles_review:
        str_re = ''
        for str_line in line:
            str_re = str_re + ' ' + str_line  # 将列表元素变为字符串
        corpus_str.append(str_re)
            # print(type(line))  # list
    for line in corpus_str:
        print(line)
    # 格式转化完成

    # TF-IDF
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
    vectorizer.fit_transform(corpus_str))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

    print(u'weight的长度', len(weight))
    # 写入txt
    list_tfidf = []
    file = "tf-idf_roles_2.txt"
    print_tidif(file, word, weight, list_tfidf)

    # 有符合条件的TDIDF值的词语的评论标号
    # 排序，顺序是乱的
    # new_list_tfidf=list(set(list_tfidf))
    # 排序 正序
    new_list_tfidf = []
    for line in list_tfidf:
        if line not in new_list_tfidf:
            new_list_tfidf.append(line)
    print(new_list_tfidf)
    print(len(new_list_tfidf))  #符合要求的评论数量