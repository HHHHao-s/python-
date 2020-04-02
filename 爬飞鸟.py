import requests
from lxml import html
import time
import os
from multiprocessing.dummy import Pool
os.chdir(r'C:\Users\Administrator\Desktop\Python\爬')
os.mkdir('飞鸟3')
os.chdir('飞鸟3')


def download(each):
    img_name=each.split('/')[-1]
    with open(img_name,'wb') as f:
        f.write(requests.get(each).content)
        print('downloading...%s' % (img_name))
        
etree=html.etree
#url = 'https://www.douban.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
url = 'https://www.nogizaka46.net.cn/pic/nogizaka/getImageUrl?name=asuka02.txt'
r = requests.get(url,headers = headers)
li_1 = eval(r.text)[0]["urls"]
#selector = etree.HTML(htm)
#li_1 = selector.xpath('//*[@id="dowebok"]/li/img/@src')
pool = Pool()
pool.map(download,li_1)
pool.close()
pool.join()