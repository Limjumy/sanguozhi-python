#!/usr/bin/python
# encoding:utf-8

# 将元组数据 调整表示成 词向量（词语为行按编号，词频为列，一行表示一个评论）
    # 化为[[2,2,0,0],[2,3,4]]
# 将[(0,2),(1,2)]变为[2,2,0,0,0,0,0,0,0....]
corpus=[[(0, 2), (1, 2)], [(2, 22), (3, 1), (4, 1), (5, 2), (6, 11)], []]
print(len(corpus[2]))
print('length')
yuanzu2list=[]
for line in corpus: # [(0,2),(1,2)]
    yuanzu2list.append([])
    for i in range(10):
        yuanzu2list[-1].append(0)
    print("len")
    print(len(line))
    if len(line)==0:
        continue
    print(yuanzu2list)
    for yuanzu in line:
        print('yuanzu')
        print(yuanzu[0])
        yuanzu2list[-1][yuanzu[0]] = yuanzu[1]

        print(yuanzu2list)
print(yuanzu2list)