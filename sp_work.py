#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wenzhen

# 数据导入
import json
with open('./2021_baidu/baidu_cws.json', 'r', encoding='utf-8') as g:
    baidu_cws = json.load(g)  # 词性标注结果
baidu_cws_union = [a for sublist in baidu_cws for a in sublist]
with open('./2021_baidu/baidu_pos.json', 'r', encoding='utf-8') as g:
    baidu_pos = json.load(g)  # 词性标注结果
baidu_pos_union = [a for sublist in baidu_pos for a in sublist]

# 词性统计
# import pprint
# # 经典的统计并排序方法
# pos_set = list(set(baidu_pos_union))
# pos_dict = {}
# for pos in pos_set:
#     pos_dict.update({pos: baidu_pos_union.count(pos)})
# # sorted(zip())对字典按值排序,输出为列表
# pos_stat = sorted(zip(pos_dict.values(), pos_dict.keys()), reverse=True)
# with open('./data_stat/pos_stat.txt', 'w', encoding='utf-8') as f:
#     f.write(pprint.pformat(pos_stat))

# 各词性代表词统计
pos_symbol_word = {}  # 存储为{词性: 对应词的列表}
for cws, pos in zip(baidu_cws_union, baidu_pos_union):
    if pos in pos_symbol_word:
        pos_symbol_word[pos].append(cws)
    else:
        pos_symbol_word.update({pos: [cws]})
for key in pos_symbol_word.keys():
    temp = list(set(pos_symbol_word[key]))
    temp_dict = {}
    for word in temp:
        temp_dict.update({word: pos_symbol_word[key].count(word)})
    temp_list = sorted(zip(temp_dict.values(), temp_dict.keys()), reverse=True)
    pos_symbol_word[key] = temp_list  # 修正为{词性: [(对应词: 出现次数)]}

with open('./data_stat/pos_symbol_word.json', 'w', encoding='utf-8') as f:
    json.dump(pos_symbol_word, f, ensure_ascii=False)
