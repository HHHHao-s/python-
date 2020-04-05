import requests
import os
import re
from lxml import html
import easygui as e
from multiprocessing.dummy import Pool
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    ,'Referer': 'https://space.bilibili.com/327621460/album'
}
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

def getzlurl(search,page1,page2):
    for n in range(page1,page2+1):
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
    if choose == '1.爬取相簿':#用户爬取相簿
        user_id = input('请输入需要爬取的用户:')
        os.chdir(e.diropenbox('选择存放地址'))
        n = 0
        pool = Pool()
        for picurls,name in getpicurl(user_id):
            n += 1
            if not os.path.exists(name):
                try:
                    os.mkdir(name)
                    os.chdir(name)
                except OSError:
                    if not os.path.exists('错误标题'):
                        os.mkdir('错误标题')
                    os.chdir('错误标题')
            pool.map(download,picurls)
            os.chdir('..')
        pool.close()
        pool.join()
    if choose == '2.爬取专栏':#专栏爬取
        search = e.enterbox('请输入要搜索的内容')
        page = e.multenterbox('请输入页数范围',fields = ['开始','结束'])
        url_dict = getzlurl(search,int(page[0]),int(page[1]))
        pool = Pool()
        os.chdir(e.diropenbox('请选择存放地址'))
        for name,url in url_dict.items():
            try:
                os.mkdir(name)
            except BaseException as reason:
                print(reason)
                if not os.path.exists('错误标题'):
                    os.mkdir('错误标题')
                name = '错误标题'
            os.chdir(name)
            picurls = getzlpicurl(url)
            pool.map(download,picurls)
            os.chdir('..')
        pool.close()
        pool.join()

if __name__ == '__main__':
    while True:
        choose = e.buttonbox('请选择功能',choices=['1.爬取相簿','2.爬取专栏'])
        if choose != None:
            main(choose)
            e.msgbox('下载完成')
        else:
            pass