import os
import time
import easygui as e
from multiprocessing.dummy import Pool

import requests
from lxml import html

etree = html.etree
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Referer': 'https://music.163.com/'
}


def download(name, id, artist):
    if len(name) > 20:
        name = name[:20]
    if len(artist) > 10:
        artist = artist.split('/')[0]
    path = os.getcwd() + '\\' + name + '-' + artist + '.mp3'
    url = 'http://music.163.com/song/media/outer/url?id=' + id + '.mp3'
    try:
        with open(path, 'wb') as f:
            print('downloading...', str(id))
            html = requests.get(url, headers=headers)
            f.write(html.content)
    except:
        pass


def download1(other):
    download(other[0], other[1], other[2])


def getlist(id, type='1.添加'):  # 0为获取歌手名,1为不获取(获取歌手名用时长)
    print('processing...')
    response = requests.get(
        "https://music.163.com/playlist?id=" + id, headers=headers)
    response.encoding = 'utf-8'
    s = etree.HTML(response.text)
    list_name = s.xpath('//*[@name="keywords"]/@content')[0].split('，')[0]
    music_id = list(map(lambda x: x.split(
        '=')[-1], s.xpath('//ul[@class="f-hide"]/li/a/@href')))
    music_name = s.xpath('//ul[@class="f-hide"]/li/a/text()')
    music_artist = []
    for id in music_id:
        if type == '1.添加':
            artist = etree.HTML(requests.get('https://music.163.com/song?id=' + id,
                                             headers=headers).text).xpath('//*[@property="og:music:artist"]/@content')[0]
            music_artist.append(artist)
        if type == '0.不添加（速度较快）':
            music_artist.append('')
    play_list = [(x, music_id[music_name.index(x)],
                  music_artist[music_name.index(x)]) for x in music_name]
    return play_list, list_name


def main():
    id = e.enterbox('请输入歌单id:')
    pool = Pool()
    type = e.buttonbox("是否添加作者名:", "", ['0.不添加（速度较快）', '1.添加'])
    play_list, list_name = getlist(id, type)
    print(play_list)
    path = e.diropenbox('请选择存放地址')
    os.chdir(path)
    if not os.path.exists(list_name):
        try:
            os.mkdir(list_name)
        except:
            list_name = e.enterbox("请自行输入文件名")
            os.mkdir(list_name)
    os.chdir(list_name)
    pool.map(download1, play_list)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()


'''
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple lxml
安装库
'''