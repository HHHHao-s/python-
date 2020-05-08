import requests
import os
import re
import time
from lxml import html
from multiprocessing.dummy import Pool as pl
etree = html.etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Referer': 'https://www.huashi6.com/draw/173632'
}


def geturl(range_):
    a, b = range_.split('-')
    for n in range(a, b + 1):
        time.sleep(1)
        url = 'https://www.huashi6.com/hot' + '_' + str(n)
        r = requests.get(url, headers=headers)
        picurl = re.findall(
            '<img src="(.*?)" alt=".*?" data-original="" title=".*?" class="c-img-loading">', r.text)
        yield picurl


def download(picurl):
    time.sleep(1)
    file_name = picurl.split('/')[-1]
    if not os.path.exists(file_name):
        try:
            pic = requests.get(picurl, headers=headers, timeout=5).content
            with open(file_name, 'wb') as f:
                f.write(pic)
                print('downloading...%s\n' % file_name)
        except BaseException as reason:
            print(reason)


def main():
    range_ = input('请输入下载范围(xxx-xxx):')
    os.chdir(os.getcwd())
    try:
        os.mkdir('画师通')
    except:
        pass
    os.chdir('画师通')
    pool = pl()
    for each in geturl(range_):
        each = list(map(lambda x: x.split('src="')[-1], each))
        pool.map(download, each)
    pool.close()
    pool.join()
    print('下载完成')


if __name__ == '__main__':
    main()
