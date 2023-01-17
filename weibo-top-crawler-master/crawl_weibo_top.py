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
    for title, hot_index, rank, type1 in records:
        time_count_dict = {'time': time_str, 'hot_index': hot_index, 'rank':
            rank, 'type': type1}
        dict_obj.setdefault(title, []).append(time_count_dict)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict_obj, f, indent=4, separators=(',', ': '),
                  ensure_ascii=False, sort_keys=False)


def crawl_weibo_top():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Host': 's.weibo.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh-HK;q=0.8,zh;q=0.7,en;q=0.6,fr;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        # 定期更换Cookie
        'Cookie': 'UOR=www.baidu.com,weibo.com,www.baidu.com; SINAGLOBAL=8881262834522.79.1667654142836; PC_TOKEN=82db33ad87; SCF=Ai-yyMF1rZZGb617lQIPK-ilwIeWIGxqb3ITWAbQt2fRiRzclnTM2aCpTp2Uf6Ky7dEMPJPkHeODerKDXr_dPe0.; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5om16E7eXanCvaCrXQDZn_5JpVF02fSoqESo-ESoec; SUB=_2AkMUmlJOdcPxrARTkPkRyWzna4tH-jynTzu4An7uJhMyAxh87kcsqSVutBF-XMJ-uc32ZHwcLFs9om9T4-eW0yXg; _s_tentry=-; Apache=6360731486994.88.1673977687245; ULV=1673977687267:11:5:3:6360731486994.88.1673977687245:1673952579169'
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    record_tags = soup.find_all('tr')
    titles, hot_indices, ranks, types = [], [], [], []
    for item in record_tags:
        tag = item.find('td', {'class': 'td-02'})
        rank = item.find('td', {'class': 'ranktop'})
        if (tag is not None) and (rank is not None) and (rank.text.strip() !=
                                                         "•"):
            titles.append(tag.a.text.strip())
            ranks.append(rank.text.strip())
            if len(tag.span.text.split()) == 2:
                types.append(tag.span.text.split()[0])
                hot_indices.append(tag.span.text.split()[1])
            else:
                types.append('None')
                hot_indices.append(tag.span.text.split()[0])
    return titles, hot_indices, ranks, types


if __name__ == '__main__':
    now = get_utc8now()
    year_str = now.strftime('%Y')
    date_str = now.strftime('%Y%m%d')
    os.makedirs(year_str, exist_ok=True)
    filename = os.path.join(year_str, '{} 微博实时热搜.json'.format(date_str))

    titles, hot_indices, ranks, types = crawl_weibo_top()
    records = list(zip(titles, hot_indices, ranks, types))
    save_as_json(filename, records)
