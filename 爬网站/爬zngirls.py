import requests
import os
import easygui as e
from multiprocessing.dummy import Pool
from lxml import html

etree = html.etree

os.chdir('D:\\爬爬爬')
head_url = 'https://www.nvshens.net/gallery/bololi/#'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    , 'Referer': 'https://www.nvshens.net/gallery/ugirl/2.html'
}


def getfirst_url(head_url):
    response1 = requests.get(head_url, headers=headers)
    response1.encoding = 'utf-8'
    s = etree.HTML(response1.text)
    second_url = s.xpath('//*[@class="galleryli"]/div[2]/a/@href')
    return second_url  # 网址


def getpeople(head_url):  # 专门的人
    try:
        head_url = head_url + 'album/'
        r = requests.get(head_url)
        s = etree.HTML(r.text)
        pagen = s.xpath('//*[@id="post_entry"]/div[3]/div/a[2]/@href')
        urls = []
        each_url = s.xpath('//*[@id="photo_list"]/ul/li/div[1]/a/@href')
        urls.extend(each_url)
        for each in pagen:
            
            each = 'https://www.nvshens.net' + each
            r = requests.get(each,headers = headers)
            s = etree.HTML(r.text)
            each_url = s.xpath('//*[@id="photo_list"]/ul/li/div[1]/a/@href')
            urls.extend(each_url)
        print(urls)
        return urls#返回每一个second_url
    except BaseException as reason:
        print(reason)


def getsecond_url(url):
    try:
        response = requests.get(url, headers=headers, timeout=7)
        s = etree.HTML(response.text)
        pagen = s.xpath('//*[@id="dinfo"]/span/text()')[0]
        name = s.xpath('//*[@id="htilte"]/text()')[0]
        if not os.path.exists(name):
            os.mkdir(name)
            os.chdir(name)
            n = int(pagen[0]) * 10 + int(pagen[1])
            page_number = (n + 2) // 3  # 推算出总页数
            for each in range(1, page_number + 1):
                each_url = ('https://www.nvshens.net/g/' + url.split('/')[-2] + '/' + str(each) + '.html')
                s1 = etree.HTML(requests.get(each_url, headers=headers).text)
                pic_url = s1.xpath('//*[@id="hgallery"]/img/@src')
                pic = []
                for eachpic in pic_url:
                    eachpic = eachpic.replace('/s', '')
                    pic.append(eachpic)
                    print('gettingpic...')
                yield pic  # 返回存放图片高清地址的列表
    except BaseException as reason:
        print(reason)


def download(url):
    try:
        r = requests.get(url, headers=headers,timeout = 7)
        file_name = url.split('/')[-1]
        with open(file_name, 'wb') as f:
            f.write(r.content)
            print('downloading...%s' % file_name)
    except BaseException as reason:
        print(reason)


def main(head_url):
    first_dict = getfirst_url(head_url)
    for second_url in first_dict.items():
        try:
            for pic_list in getsecond_url(second_url):
                for eachpic in pic_list:
                    download(eachpic)
            os.chdir('..')
        except BaseException as reason:
            print(reason)


def main2(head_url):
    urls = getpeople(head_url)
    for url in urls:
        try:
            url = 'https://www.nvshens.net/' + url
            for pic_list in getsecond_url(url):
                pool.map(download,pic_list)
            os.chdir('..')
        except BaseException as reason:
            print(reason)
        finally :
            os.chdir('D:\\爬爬爬')
    pool.close()
    pool.join()

def main3(head_url):
    for each_url in getsecond_url(head_url):
        pool.map(download,each_url)
    pool.close()
    pool.join()


if __name__ == '__main__':
    pool = Pool(3)
    choose = input('1.下载菠萝社，2.搜索人物,3.下载特定网页:')#21501
    if choose == '1':
        n = input('输入下载范围（xx-xx）:')
        a, b = n.split('-')
        for each in range(int(a), int(b) + 1):
            head_url = 'https://www.nvshens.net/gallery/bololi/2.html'.replace('2', n)
            if each == 1:
                head_url = 'https://www.nvshens.net/gallery/bololi/'
            main(head_url)
    if choose == '2':
        search = input('请输入要下载的对象的id:')
        head_url ='https://www.nvshens.net/girl/' + search + '/'
        main2(head_url)
    if choose == '3':
        head_url = input('请输入下载的网页:')
        main3(head_url)

# 可供参考地址https://www.nvshens.net/gallery/
