import math
import urllib.request
import gzip
import json
import easygui as e
import os
import sys
import cloudmusic
import time,datetime
def get_weather_data() :
    print('------天气查询------')
    city_name = str(e.enterbox('请输入要查询的城市名称：','天气系统','佛山'))
    url1 = 'http://wthrcdn.etouch.cn/weather_mini?city='+urllib.parse.quote(city_name)
    url2 = 'http://wthrcdn.etouch.cn/weather_mini?citykey=101010100'
    #网址1只需要输入城市名，网址2需要输入城市代码
    #print(url1)
    weather_data = urllib.request.urlopen(url1).read()
    #读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    #解压网页数据
    weather_dict = json.loads(weather_data)
    #将json数据转换为dict数据
    return weather_dict

def show_weather(weather_data):
    weather_dict = weather_data
    #将json数据转换为dict数据
    if weather_dict.get('desc') == 'invilad-citykey':
        e.msgbox('你输入的城市名有误，或者天气中心未收录你所在城市','查询错误')
    elif weather_dict.get('desc') =='OK':
        text=''
        forecast = weather_dict.get('data').get('forecast')
        text+=('城市：'+ weather_dict.get('data').get('city')+'\n')
        text+=('温度：'+ weather_dict.get('data').get('wendu') + '℃ '+'\n')
        text+=('感冒：'+ weather_dict.get('data').get('ganmao')+'\n')
        text+=('风向：'+ forecast[0].get('fengxiang')+'\n')
        text+=('风级：'+ forecast[0].get('fengli')+'\n')
        text+=('高温：'+ forecast[0].get('high')+'\n')
        text+=('低温：'+ forecast[0].get('low')+'\n')
        text+=('天气：'+ forecast[0].get('type')+'\n')
        text+=('日期：'+ forecast[0].get('date')+'\n')
        text+=('*******************************')
        e.msgbox(text)
        show()

def suanshu():
    list1=['1:二元一次方程','2:使用系统计算机','3.阶乘']
    xuanxiang = e.buttonbox(msg='请选择使用方式',title='算术系统',choices=list1)
    if xuanxiang==list1[0]:
        result=''
        list2=['二次项系数a','一次项系数b','常数c']
        a,b,c=e.multenterbox('请输入各项系数','二元一次方程',list2,'')
        a,b,c=int(a),int(b),int(c)
        w =b**2-4*a*c
        if w < 0:
            result='无解'
        elif w > 0:
            x1 = ((-b) + ((w) ** (1 / 2))) / (2 * a)
            x2 = ((-b) - ((w) ** (1 / 2))) / (2 * a)
            result+=str(x1)
            result+=' '+str(x2)
        elif w == 0:
            x3 = -b / (2 * a)
            result=x3
        if w >= 0:
            e.msgbox(result,'结果')
    if xuanxiang==list1[1]:
        os.system('calc.exe')
    if xuanxiang==list1[2]:
        enter=int(e.enterbox('请输入要求的阶乘数','阶乘系统',''))
        x=1
        if enter>1:
            for each in range(1,enter+1):
                x*=each
        elif enter==1:
            pass
        else:
            x=0
        if x:
            e.msgbox('结果为:'+str(x),'阶乘系统')
        else:
            e.msgbox('输入错误','阶乘系统')
    show()

def search_file():
        name=e.enterbox('请输入要搜索的文件名或类型','文件搜索系统')
        if not name==None:
            path=str(e.diropenbox('请寻找文件根目录'))
            os.chdir(path)
            each_dir=os.walk(os.getcwd())
            msg=''
            for each in each_dir:
                for each_file in each[2]:
                    if os.path.splitext(each_file)[1] == name or each_file == name:
                        msg+=(os.path.join(os.getcwd(),each_file))+'\n'
            if msg:e.msgbox(msg,'搜索结果')
            else:e.msgbox('未找到文件')
        else:
            pass
        show()
        
def getmusic():
    choice=['1.获取歌单信息','2.获取个人信息','3.退出本系统']
    choose=e.buttonbox('请选择操作','网易云音乐系统',choice)
    if choose == choice[0]:
        list_id = e.integerbox('请输入歌单的id','网易云音乐系统',upperbound=999999999)
        try:
            play_list=cloudmusic.getPlaylist(list_id)
        except:
            e.msgbox('获取失败，请输入正确的歌单id')
            getmusic()
        choice1=['1.下载歌单','2.退出本程序']
        msg=''
        for each in play_list:
            msg+=each.name+'\n'
        choose=e.buttonbox('歌曲名如下:\n'+msg,'请选择接下来的操作',choice1)
        if choose==choice1[0]:
            dir=e.diropenbox('请选择存放地址')
            os.chdir(dir)
            e.msgbox('点确定以开始下载','网易云音乐系统')
            for music in play_list:
                music.download(level='lossless')
            e.msgbox('下载完成')
        elif choose==choice1[1]:
            pass
    elif choose == choice[1]:
        id=e.integerbox('请输入要查找的id','网易云音乐系统','515694669',upperbound = 999999999)
        if id==None:
            getmusic()
        user=cloudmusic.getUser(id)
        msg=''
        dict1={'id':'用户id',
            'level':'用户等级',
            'listenSongs':'累计听歌数量',
            'createTime':'账号创建时间',
            'nickname':'用户昵称',
            'avatarUrl':'头像url',
            'city':'所在城市的行政区划代码',
            'province':'所在省份的行政区划代码',
            'vipType':'vip类型',
            'birthday':'生日时间戳',
            'signature':'个性签名',
            'fans':'粉丝数量',
            'follows':'关注的用户数量',
            'eventCount':'动态数量',
            'playlistCount':'创建的歌单数量'}
        for key,value in dict1.items():     
                msg+=str(value)+':'+str(eval('user.'+str(key)))+'\n'
        choice=['1.获取用户的歌单(下载)','2.退出本程序']
        choose=e.buttonbox('信息如下:\n'+msg,'网易云音乐系统',choice)
        if choose == choice[0]:
            msg=''
            playlist=user.getPlaylist()
            n=0
            for each in playlist:
                msg+=str(n)+'.'+each['name']+'\n'
                n+=1
            choice=['1.下载歌单','2.退出本程序']
            choose=e.buttonbox('歌单名称:\n'+msg,'网易云音乐系统',choice)#515694669
            if choose==choice[0]:
                tips='请选择下载的范围\n'
                list_range=e.enterbox(tips+msg+'(请用“，”将各歌单分割，如“1-2，3，4”)','网易云音乐系统')
                print(list_range)
                if list_range==None:getmusic()
                list1=[]
                if ',' or '，' in list_range:#将范围分割
                    list_range=list_range.replace('，',',')
                    list_range=list_range.split(',')
                    print(list_range)
                    for each in list_range:
                        if '-' in each:
                            a,b=each.split('-')
                            list_range.remove(each)
                            for i in range(int(a),int(b)+1):
                                list1.append(i)
                        else:
                            list1.append(int(each))
                elif '-' in list_range:
                     a,b=list_range.split('-')
                     for i in range(int(a),int(b)+1):
                        list1.append(i)
                else:
                    list1.append(int(list_range))
                list1=list(set(list1))
                if e.ccbox('歌单范围是%s,点按continue开始下载' % str(list1)):
                    try:
                        dir=e.diropenbox('请选择存放地址')
                        for i in list1:      
                            dirname=playlist[int(i)]['name']
                            dirs=os.path.join(dir,dirname)
                            os.mkdir(dirs)
                            os.chdir(dirs)
                            download_music(playlist[int(i)]['id'])
                            os.chdir(dir)
                    except:
                        getmusic()
                    
        elif choose == choice[1]:
            pass
        
    show()
    
def download_music(list_id):
        try:
            play_list=cloudmusic.getPlaylist(list_id)
            for music in play_list:
                music.download(level='lossless')
            print('下载完成')
        except:
            print('获取失败，请输入正确的歌单id')
        



def show():
    list1=['1.算术','2.天气查询','3.搜索文件','4.网易云音乐系统','5.扫雷','6.退出程序']
    choice=e.buttonbox('请选择','欢迎来到豪哥系统',list1)
    if choice == list1[0]:suanshu()
    elif choice == list1[1]:show_weather(get_weather_data()) 
    elif choice == list1[2]:search_file()
    elif choice == list1[3]:getmusic()
    elif choice == list1[5]:sys.exit()
   
   









show()

