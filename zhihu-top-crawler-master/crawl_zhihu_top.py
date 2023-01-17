#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Wenzhen
import json
import os
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
from datetime import timezone

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
    for title, url, hot_index, rank, excerpt in records:
        time_count_dict = {'time': time_str, 'hot_index': hot_index, 'rank':
            rank, 'excerpt': excerpt, 'url': url}
        dict_obj.setdefault(title, []).append(time_count_dict)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict_obj, f, indent=4, separators=(',', ': '),
                  ensure_ascii=False, sort_keys=False)


def crawl_weibo_top():
    url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50'
    response = requests.get(url)
    soup = json.loads(response.text)
    titles, urls, hot_indices, ranks, excerpts = [], [], [], [], []
    for i, item in enumerate(soup['data']):
        titles.append(item['target']['title'])
        urls.append('https://www.zhihu.com/question/' + str(item['target'][
                                                                'id']))
        hot_indices.append(item['detail_text'])
        ranks.append(str(i + 1))
        excerpts.append(item['target']['excerpt'])
    return titles, urls, hot_indices, ranks, excerpts


if __name__ == '__main__':
    now = get_utc8now()
    year_str = now.strftime('%Y')
    date_str = now.strftime('%Y%m%d')
    os.makedirs(year_str, exist_ok=True)
    filename = os.path.join(year_str, '{} 知乎实时热榜.json'.format(date_str))

    titles, urls, hot_indices, ranks, excerpts = crawl_weibo_top()
    records = list(zip(titles, urls, hot_indices, ranks, excerpts))
    save_as_json(filename, records)
