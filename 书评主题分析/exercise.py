#!/usr/bin/python
# encoding:utf-8

# 用Anaconda来跑
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop=set(stopwords.words('english'))
exclude=set(string.punctuation)
lemma=WordNetLemmatizer()

# 数据准备
doc1="Sugar is bad to consume.My sister likes to have sugar,but not my father."
doc2="My father spends a lot of time driving my sister around to dance practice."
doc3="Doctors suggest that driving may cause increased stress and blood pressure."
doc4="Sometimes I feel pressure to perform well at school,but my father never seems to drive my sister to do better."
doc5="Health experts say that Sugar is not good for your lifestyle."

#compile documents
doc_complete=[doc1,doc2,doc3,doc4,doc5]

# 数据清洗
def clean(doc):
    stop_free=" ".join([i for i in doc.lower().split() if i not in stop])
    punc_free=''.join(ch for ch in stop_free if ch not in exclude)
    normalized=" ".join(lemma.lemmatize(word) for word in punc_free.strip())
    return normalized

doc_clean=[clean(doc).split() for doc in doc_complete]

# 计算文档词频矩阵
from gensim import corpora
import gensim
dictionary=corpora.Dictionary(doc_clean)
corpus=[dictionary.doc2bow(doc) for doc in doc_clean]# doc_term_matrix

# 构建LDA模型
Lda=gensim.models.ldamodel.LdaModel
ldamodel=Lda(corpus,num_topics=3,id2word=dictionary,passes=50)

# 拟合结果
print(ldamodel.print_topics(num_topics=3,num_words=3))

