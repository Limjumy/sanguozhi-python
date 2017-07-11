#!/usr/bin/python
# encoding:utf-8


import jieba
import codecs
import jieba.posseg as pseg

names = {}
relationships = {}
line_name_v = []

# 将 人物与动词 进行词共现组合
# 如何筛选这个人物的附近动词？段落似乎不可取，因为段落中是所有出现的人物的动词
# 以段落为单位，记录出现的人物以及动词 于列表line_name_v内，列表内嵌入字典{w.word:w.flag}
# 以人物为单位，搜寻人物周围的动词，记录动词w.word于 列表 人物名字role_v_cc 如曹操

# jieba.load_userdict("names_sanguo.txt")  # 加载字典

#def get_cixing(word,flag):# 通过jieba.poss记录位置的函数？


with codecs.open("bhsgz.txt", "r", "utf-8") as f:
    for line in f.readlines():
        poss = pseg.cut(line)  # 分词并返回该词词性
        line_name_v.append([])  # 为新读入的一段添加人物名称列表
        for w in poss:
            if w.flag != "na" and w.flag != "v":
                continue
            line_name_v[-1].append({w.word:w.flag})  # 为当前段的环境增加一个人物
            if names.get(w.word) is None:
                relationships[w.word] = {}
            #names[w.word] += 1  # 该人物出现次数加 1

print line_name_v

# explore relationships
#for line in line_name_v:  # 对于每一段，因为readlines就是一段一段地读取文本，不是一行一行。
#    for name1 in line:
#        for name2 in line:  # 每段中的任意两个人
 #           if name1 == name2:
 #               continue
 #           if relationships[name1].get(name2) is None:  # 若两人尚未同时出现则新建项
 #               relationships[name1][name2] = 1

 #           else:
  #               relationships[name1][name2] = relationships[name1][name2] + 1  # 两人共同出现次数加 1




# output 打印line_name_v
with codecs.open("name_v.txt", "a+", "utf-8") as f:
    #f.write("Source Target Weight\r\n")
    for line in line_name_v: # 对于每一段
        for w in line:
            print w
            for word, flag in w.items():
                f.write(word + " " + str(flag) + " "+"\r\n")

        f.write('\r\n')# 每一段结束，空一行
