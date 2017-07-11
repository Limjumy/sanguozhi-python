#!/usr/bin/python
# encoding:utf-8

##########NONONONONO!!
#借鉴 sanguozhi_pa_changpl.py 爬虫获取文章以及编号

import re
import requests
from multiprocessing import Pool

from requests.exceptions import RequestException

from gensim import corpora, models, similarities # 主题分析

# 修改正则表达式后，程序运行很快，93条长评论
# 去合适的网页打印出所需要的用户评论，且每条评论写入不同的txt中
# 将编码存入列表
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<div.*?main-bd.*?>.*?<div.*?review\w(.*?)\wshort.*?>', re.S)
    items = re.findall(pattern, html)
    return items #是列表，此处返回每一页评论编号


def add_urll(urll,list):# 爬取长评论，将list的元素加入urll ,这里list是列表的元素 即bianhao[0]
    urll=urll+list
    return urll


def main(offset,list):
    bianhao=[]
    a=[]
    url = 'https://book.douban.com/subject/1926289/reviews?start='+ str(offset)
    urll='https://book.douban.com/review/'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        bianhao.append(item) #bianhao 为每一页长评论的编码，一次循环是一页
    print(bianhao)
    # 爬取长评论
    for line in bianhao:# 对于每一页的每一个编码，遍历
        urll = add_urll(urll, line)  # urll为网址,line是列表的每个元素
        print(urll)

        content = requests.get(urll).text
        urll='https://book.douban.com/review/'
        # 筛选长评论 推荐等级（几颗星“力荐”）及其标题
        pattern = re.compile(
            '<h1.*?summary.*?>(.*?)</span>.*?<span.*?allstar.*?title="(.*?)"></span>.*?<div.*?review-content.*?>.*?(.*?)<script.*?text.*?>', re.S)
        results = re.findall(pattern, content)

        # 爬取得到的评论，放入列表中
        list.append(results)
    return list




if __name__ == '__main__':
    document=[]
    pool = Pool()
    document=pool.map(main, [i*20 for i in range(5)])#5页
    pool.close()
    pool.join()

    print(document)