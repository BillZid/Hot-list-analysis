#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wenzhen

import json

from ltp import LTP

ltp = LTP("LTP/legacy")

ltp.add_words('新冠', freq=2)
# 将模型移动到 GPU 上
# if torch.cuda.is_available():
#     # ltp.cuda()
#     ltp.to("cuda")

with open('./2021_baidu/baiduresou2021.json', 'r', encoding='utf-8') as f:
    baidu = json.load(f)
baidu_title = list(baidu.keys())
cws, pos, ner = ltp.pipeline(baidu_title, tasks=["cws", "pos",
                                                 "ner"]).to_tuple()

with open('./2021_baidu/baidu_cws.json', 'w', encoding='utf-8') as g:
    json.dump(cws, g, ensure_ascii=False, indent=4)
with open('./2021_baidu/baidu_pos.json', 'w', encoding='utf-8') as g:
    json.dump(pos, g, ensure_ascii=False, indent=4)
with open('./2021_baidu/baidu_ner.json', 'w', encoding='utf-8') as g:
    json.dump(ner, g, ensure_ascii=False, indent=4)
