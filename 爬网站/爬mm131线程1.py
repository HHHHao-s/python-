import requests, os, sys
from multiprocessing.dummy import Pool as pl
import time
from lxml import html

etree = html.etree

try:
    os.mkdir('F:\\爬爬爬')
except:
    pass
os.chdir('F:\\爬爬爬')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    , 'Referer': 'https://www.mm131.net/qingchun/5175_2.html'
}

url_all = []


def geturl(url):
    rf = requests.get(url, headers=headers)  # 在这修改网址
    sf = etree.HTML(rf.text)
    url_all.extend(sf.xpath('//*[@target="_blank"]/@href'))  # 具体网址，列表


def download(each):
    r = requests.get(each, headers=headers)
    s = etree.HTML(r.text)
    times = s.xpath('//*[@class="content-page"]/span[1]/text()')
    try:
        times = (int(str(times)[4] + str(times)[5]))
        try:
            r.encoding = 'GBK'
            s1 = etree.HTML(r.text)
            os.chdir('F:\\爬爬爬')
            name = os.getcwd() + '\\' + s1.xpath('/html/body/div[5]/h5/text()')[0]
            os.mkdir(name)
        except:
            pass
        os.chdir(name)
        for i in range(2, times):
            replace1 = each.split('/')[-1].split('.')[0] + '_' + str(i)
            urls = each.replace(each.split('/')[-1].split('.')[0], replace1)
            r1 = requests.get(urls, headers=headers)
            s3 = etree.HTML(r1.text)
            pic1 = s3.xpath('//*[@class="content-pic"]/a/img/@src')
            file_name = pic1[0].split('/')[-1]
            r2 = requests.get(pic1[0], headers=headers)
            with open(file_name, 'wb') as f:
                f.write(r2.content)
                print('downloading......')
    except:
        pass


def main():
    url_list = []
    for i in range(2, 10):
        url = 'https://www.mm131.net/xinggan/list_6_2.html'.replace('2', str(i))
        url_list.append(url)
    return url_list


if __name__ == '__main__':
    url_list = main()
    pool = pl()
    pool.map(geturl, url_list)
    pool.close()
    pool.join()
    pool = pl()
    pool.map(download, url_all)
    pool.close()
    pool.join()
    print('下载完成')

#download('https://www.mm131.net/xinggan/2260.html')