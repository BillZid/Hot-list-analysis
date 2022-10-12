#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wenzhen

import json
import pprint
import numpy as np
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel

with open('./2021_baidu/baidu_cws.json', 'r', encoding='utf-8') as g:
    baidu_cws = json.load(g)  # 分词结果
with open('./2021_baidu/baidu_pos.json', 'r', encoding='utf-8') as g:
    baidu_pos = json.load(g)  # 词性标注结果
# with open('./stopwords/hit_stopwords.txt', 'r', encoding='utf-8') as g:
#     stopwords = [word.rstrip('\n') for word in g.readlines()]
with open('./stopwords/stopwords.txt', 'r', encoding='utf-8') as g:
    stopwords = [word.rstrip('\n') for word in g.readlines()]
with open('./stopwords/self_stopwords.txt', 'r', encoding='utf-8') as g:
    stopwords += [word.rstrip('\n') for word in g.readlines()]

for i in range(len(baidu_cws))[::-1]:
    for j in range(len(baidu_cws[i]))[::-1]:
        if baidu_pos[i][j] not in ['nh', 'n', 'v', 'j', 'ns', 'ni', 'nz'] or \
                baidu_cws[i][j] in stopwords or len(baidu_cws[i][j]) < 2:
            del baidu_cws[i][j]
            del baidu_pos[i][j]

dictionary = corpora.Dictionary(baidu_cws)  # 构建词典
# dictionary.save('./models/baidu_dictionary.dict')  # 存储词典
corpus = [dictionary.doc2bow(title) for title in baidu_cws]  # 把标题转化为bow向量
# corpora.MmCorpus.serialize('./models/baidu_corpus.mm', corpus)  # 存储语料库
# corpus_tfidf = TfidfModel(corpus)[corpus]  # 转化为TfIdf替代频次
coherence_cv = []
# 对不同主题数应用LDA
for num_topics in range(19, 20):
    n = str(num_topics)  # 利用exec和占位符批量操作
    exec('lda_%s_model = LdaModel(corpus, num_topics=%d, id2word=dictionary,'
         'passes=50)' % (n, num_topics))
    # exec('lda_%s_model.save("./models/baidu_%s.model")' % (n, n))  # 存储LDA模型
    # f = open('./models/lda_%s_topics.txt' % n, 'w', encoding='utf-8')
    f = open('./test_models/lda_%s_topics.txt' % n, 'w', encoding='utf-8')
    exec('f.write(pprint.pformat(lda_%s_model.print_topics(num_topics=%d, '
         'num_words=50)))' % (n, num_topics))  # 存储LDA主题词
    f.close()
    # 求语义一致性,u_mass不依赖外部文本,计算更快速,但c_v准确度更高
    # exec('coherence_cv.append(CoherenceModel(model=lda_%s_model, '
    #      'texts=baidu_cws, dictionary = '
    #      'dictionary, coherence="c_v").get_coherence())' % n)
# pprint.pprint(coherence_cv)
# np.savetxt('./models/coherence_cv.txt', coherence_cv)
