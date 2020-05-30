from requests import get
from json import loads
from multiprocessing.dummy import Pool
import os
import easygui as e
class Solve:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Referer': 'https://music.163.com/'
        }


    def getid(self, list_id):  # 获取id
        url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id=' + list_id
        text = loads(get(url, headers=self.headers).text)  # 获取返回值
        ids = list(map(lambda x: str(x['id']), text['playlist']['trackIds']))
        list_name = text['playlist']['name']
        return ids, list_name

    def getdetail(self, song_id):  # 获取歌曲名以及作者
        try:
            url = 'https://api.imjad.cn/cloudmusic/?type=detail&id=' + song_id
            text = loads(get(url).text)
            detail = (text['songs'][0]['name'], text['songs']
                      [0]['ar'][0]['name'], song_id)
            self.download(detail[2], detail[0], detail[1])  # 储存
        except:
            pass

    def download(self, id, name, artist):  # 下载
        if len(name) > 20:
            name = name[:20]

        path = name + '-' + artist + '.mp3'
        url = 'http://music.163.com/song/media/outer/url?id=' + id
        f = open(path, 'wb')
        print('downloading...', name)
        html = get(url, headers=self.headers,timeout = 5)
        f.write(html.content)
        f.close()



if __name__ == "__main__":
    cool = Solve()
    list_id = e.enterbox('请输入歌单id:')
    ids, list_name = cool.getid(list_id)
    pool = Pool()
    path = e.diropenbox('请选择存放地址')
    os.chdir(path)
    if not os.path.exists(list_name):
        try:
            os.mkdir(list_name)
        except:
            list_name = e.enterbox("请自行输入文件名")
            os.mkdir(list_name)
    os.chdir(list_name)
    pool.map(cool.getdetail, ids)
    pool.close()
    pool.join()
