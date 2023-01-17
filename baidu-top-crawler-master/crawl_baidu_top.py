#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wenzhen
import os
import json
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup


def get_utc8now():
    utcnow = datetime.now(timezone.utc)
    utc8now = utcnow.astimezone(timezone(timedelta(hours=8)))
    return utc8now
    
    
def save_as_json(filename, records):
    dict_obj = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            dict_obj = json.load(f, object_pairs_hook=OrderedDict)
    time_str = str(get_utc8now())
    for title, hot_index, rank in records:
        time_count_dict = {'time': time_str, 'hot_index': hot_index, 'rank':
                           rank}
        dict_obj.setdefault(title, []).append(time_count_dict)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict_obj, f, indent=4, separators=(',', ': '),
                  ensure_ascii=False, sort_keys=False)


def crawl_baidu_top(board='realtime'):
    response = requests.get('https://top.baidu.com/board?tab={}'.format(board))
    soup = BeautifulSoup(response.text, 'html.parser')
    record_tags = soup.find_all('div', {'class': 'category-wrap_iQLoo'})
    titles, hot_indices, ranks = [], [], []
    for item in record_tags:
        title_tag = item.find('div', {'class': 'c-single-text-ellipsis'})
        hot_index_tag = item.find('div', {'class': 'hot-index_1Bl1a'})
        rank = item.find('div', {'class': 'index_1Ew5p'})
        if (title_tag is not None) and (hot_index_tag is not None) and \
                (rank is not None):
            titles.append(title_tag.text.strip())
            hot_indices.append(hot_index_tag.text.strip())
            if rank.img is not None:
                ranks.append('top')
            else:
                ranks.append(rank.text.strip())
    return titles, hot_indices, ranks


if __name__ == '__main__':
    now = get_utc8now()
    year_str = now.strftime('%Y')
    date_str = now.strftime('%Y%m%d')
    os.makedirs(year_str, exist_ok=True)
    filename = os.path.join(year_str, '{} 百度实时热点.json'.format(date_str))
    
    titles, hot_indices, ranks = crawl_baidu_top()
    records = list(zip(titles, hot_indices, ranks))
    save_as_json(filename, records)
    
    
