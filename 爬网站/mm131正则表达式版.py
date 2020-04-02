import os
import re
import sys
import time
from multiprocessing.dummy import Pool as pl

import requests
from lxml import html

etree = html.etree

try:
    os.mkdir('D:\\爬爬爬')
except:
    pass
os.chdir('D:\\爬爬爬')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    , 'Referer': 'https://www.mm131.net/qingchun/5175_2.html'
}

url_all = []

def geturlwithre(url='https://www.mm131.net/xinggan/list_6_2.html'):
    rf = requests.get(url, headers=headers)  # 在这修改网址
    sf = etree.HTML(rf.text)
    rf.encoding = 'gbk'
    text = 'asdfashasldjkflasfasdfas'
    url = re.findall(r'a target="_blank" href=".*?"',rf.text)
    for each in url:
        print(each.split('"')[-2])
geturlwithre()
