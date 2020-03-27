from lxml import html
import os
import time
import requests
os.chdir(r'C:\Users\Administrator\Desktop\Python\爬\test')


etree = html.etree
url = 'https://www.huashi6.com/hot'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
r = requests.get(url,headers=headers)
path='//*[@class="bg-img c-img-loading"]/@src'
selector = etree.HTML(r.text)
pic = selector.xpath(path)
for each in pic:
    each=each.replace(each.split('_')[-1].split('.')[0],'wk1960x1080')
    time.sleep(1)
    file_name=each.split('/')[-1]
    with open(file_name,'wb') as f:
        f.write(requests.get(each,headers=headers).content)
        print('downloading...%s\n' % file_name)