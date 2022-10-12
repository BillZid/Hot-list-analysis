#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wenzhen
import json
import os

origin_data_dir = './baidu-top-crawler-master/2021'
convert_data_dir = './2021_baidu/'
convert_data = {}
for dir in os.listdir(origin_data_dir):
    with open(os.path.join(origin_data_dir, dir), 'r', encoding='utf-8') as f:
        convert_data.update(json.load(f))
with open(os.path.join(convert_data_dir, 'baiduresou2021.json'), 'w',
          encoding='utf-8') as g:
    json.dump(convert_data, g, ensure_ascii=False, indent=4)
