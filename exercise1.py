#!/usr/bin/python
# encoding:utf-8
import codecs
line_roles_places=[['a','b','c'],['er','ee','dd'],['e','e','tt']]

with codecs.open("shiyan2_result.txt", "a+", "utf-8") as f:
    for line in line_roles_places:  # 每一个段落，即每一个列表
        f.write('new para ')
        f.write('\s')
        l2 = []
        #l2 = list(set(line))# 去重 法一：此处去重方法的缺点：顺序会乱
        for i in line:
            if not i in l2:
                l2.append(i) # 去重 法二：顺序不乱
        for list in l2:   #对于列表中的每一个元素
            f.write(list)
            f.write(' ')  # 注意空格
