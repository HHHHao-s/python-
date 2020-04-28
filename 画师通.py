import requests,os,re
import time
from lxml import html
from multiprocessing.dummy import Pool as pl
etree = html.etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    ,'Referer': 'https://www.huashi6.com/draw/173632'
}

def geturl(range_):
    n=0
    a,b = range_.split('-')
    while True:
        n += 1
        if n >= int(a):
            time.sleep(1)
            url = 'https://www.huashi6.com/hot' + '_' + str(n)
            r = requests.get(url,headers=headers)
            picurl = re.findall('<img src="(.*?)" alt=".*?" data-original="" title=".*?" class="c-img-loading">',r.text)
            yield picurl,n
        if n >= int(b):
            break

def download(picurl):
        each=picurl.replace(picurl.split('_')[-1].split('.')[0],'wk1960x1080')
        time.sleep(1)
        file_name=each.split('/')[-1]
        try:
                pic = requests.get(each,headers=headers,timeout = 5).content
                with open(file_name,'wb') as f:
                    f.write(pic)
                    print('downloading...%s\n' % file_name)
        except BaseException as reason:
                print(reason)


def main():
    range_ = input('请输入下载范围(xxx-xxx):')
    os.chdir(os.getcwd())
    os.mkdir('画师通')
    os.chdir('画师通')
    for each,n in geturl(range_):
        pool = pl()
        pool.map(download,each)
        pool.close()
        pool.join()
    print('下载完成')

if __name__ == '__main__':
    main()