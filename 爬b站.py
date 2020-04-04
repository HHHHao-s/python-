import requests
import os
import re
from lxml import html
from multiprocessing.dummy import Pool
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    ,'Referer': 'https://space.bilibili.com/327621460/album'
}
os.chdir('b站涩图')
def getpicurl(user_id):
    page_number = -1
    pic_url = []
    while True:
        page_number += 1
        t = requests.get('https://api.vc.bilibili.com/link_draw/v1/doc/doc_list?uid=%s&page_num=%s&page_size=30&biz=all' % (user_id , page_number))
        if len(t.text) == 66:
            break
        infomaition = eval(t.text)
        for items in infomaition["data"]['items']:
            name = items['description']
            for pictures in items['pictures']:
                pic_url.append(pictures['img_src'])
            yield pic_url,name.replace('\n' , '0').split('0')[0]

def download(picurl):
    pic = requests.get(picurl,headers = headers)
    pic_name = str(picurl.split('/')[-1])[-10:]
    with open(pic_name, 'wb') as f:
        f.write(pic.content)
        print('downloading... %s' % pic_name)

def getzlurl(search,page):
    for n in range(1,page+1):
        url = 'https://search.bilibili.com/article?keyword=' + search + '&page=' +str(n)
        response = requests.get(url,headers = headers)
        url_dict = {}
        for eachurl in re.findall('href=".*?" title=".*?" ',response.text):
            url,name = eachurl.split('=')[1].split('"')[-1].replace(r'//','') ,eachurl.split('=')[-1].replace('"','')
            url_dict[name] = 'https://' + url
        return url_dict

def getzlpicurl(url):
    response = requests.get(url,headers = headers)
    picurl = re.findall('src=".*?"',response.text)
    picurls = []
    for each in picurl:
        if 'https' not in each:
            each = each.replace('src="','https:')
        else:
            each = each.replace('src=','')
        if 'article' in each and '.js' not in each:
            picurls.append(each.replace('"',''))
    return picurls



def main(choose):
    if choose == '1':#用户爬取相簿
        user_id = input('请输入需要爬取的用户:')
        os.chdir('b站涩图')
        n = 0
        pool = Pool()
        for picurls,name in getpicurl(user_id):
            n += 1
            if not os.path.exists(name):
                try:
                    os.mkdir(name)
                    os.chdir(name)
                except OSError:
                    os.chdir('垃圾标题淦')
            pool.map(download,picurls)
            os.chdir('..')
        pool.close()
        pool.join()
    if choose == '2':#专栏爬取
        search = input('请输入要搜索的内容')
        page = input('请输入页数')
        url_dict = getzlurl(search,int(page))
        pool = Pool()
        for name,url in url_dict.items():
            try:
                os.mkdir(name)
            except OSError or FileNotFoundError:
                name = '垃圾标题淦'
            os.chdir(name)
            picurls = getzlpicurl(url)
            pool.map(download,picurls)
            os.chdir('..')
        pool.close()
        pool.join()

choose = input('请输入功能(1.爬取相簿,2.爬取专栏):')
main(choose)