#!/usr/bin/python
# encoding:utf-8

# 将 白话三国志 按句号切割，以句子为粒度，实现共现
import codecs
import jieba
import jieba.posseg as pseg

jieba.load_userdict("E:/python_project/三国演义/names_sanguoyy.txt")  # 加载字典
jieba.load_userdict("names_pl.txt")
#jieba.load_userdict("review_cidian.txt")

#x='我不是小二。你是么，他是。谁不是呢。'
#print(x.split('。'))

sanguoyy_sen=[]
with codecs.open("bhsgz.txt", "r", "utf-8") as f:
    for line in f.readlines(): # 读取每一段落
        line_split=line.split('。') # 以句号为分割符，切割段落，为列表形式
        sanguoyy_sen.append(line_split)

    print(len(sanguoyy_sen)) #518即段落数
    print(sanguoyy_sen) #[['\ufeff  \r\n'], ['\r\n'], ['\r\n']]


# 遍历sanguoyy_san（已经切割好的）
# 筛选其中涉及"张飞"的句子
sen_role=[]
for line in sanguoyy_sen:
    for sen in line:
        if '刘备' in sen or '玄德' in sen:  ###  人物修改看这里！！！！or '彧' in sen
            sen_role.append(sen)

print(sen_role)
print(len(sen_role))

# 对含有该人物的句子 分词，筛选形容词
# 张飞：340句
adj_role=[]
for line in sen_role:
    print(line)
    print(type(line))
    #for line_str in line:
        #print(line_str)
    poss = pseg.cut(line)  # 分词并返回该词词性
    for w in poss:
        print(w.word)
        print(w.flag)
        if w.flag != 'i': #and w.flag != 'a'
            continue  # 当分词长度小于2或该词词性不为nr时认为该词不为人名
        adj_role.append(w.word)
print(adj_role)

with codecs.open("liubei_adj_sgz.txt", "a", "utf-8") as f:
    for line in adj_role:
        f.write(line)
        f.write('\r\n')


#with codecs.open("zhangfei_sentences.txt", "a", "utf-8") as f:
#    for line in sen_role:
#        #for line_ in line:
#        f.write(line)
#        f.write('\r\n')