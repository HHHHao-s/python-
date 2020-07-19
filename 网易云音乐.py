#!/usr/bin/env python
#-*- coding:utf-8 -*-
from requests import get
from json import loads
from multiprocessing.dummy import Pool
import os
import sys
from tkinter import *
from tkinter.font import Font
from tkinter.ttk import *
from tkinter.messagebox import *
import tkinter.filedialog as tkFileDialog
#import tkinter.simpledialog as tkSimpleDialog    #askstring()


class Application_ui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Form1')
        self.master.geometry('511x197')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.IDVar = StringVar(value='歌单ID')
        self.style.configure('TID.TLabel', anchor='w', font=('宋体',10))
        self.ID = Label(self.top, text='Label1', textvariable=self.IDVar, style='TID.TLabel')
        self.ID.setText = lambda x: self.IDVar.set(x)
        self.ID.text = lambda : self.IDVar.get()
        self.ID.place(relx=0.031, rely=0.081, relwidth=0.44, relheight=0.086)

        self.PathVar = StringVar(value='下载地址')
        self.style.configure('TPath.TLabel', anchor='w', font=('宋体',10))
        self.Path = Label(self.top, text='Label1', textvariable=self.PathVar, style='TPath.TLabel')
        self.Path.setText = lambda x: self.PathVar.set(x)
        self.Path.text = lambda : self.PathVar.get()
        self.Path.place(relx=0.031, rely=0.365, relwidth=0.44, relheight=0.086)

        self.Text1Var = StringVar(value='')
        self.Text1 = Entry(self.top, textvariable=self.Text1Var, font=('宋体',10))
        self.Text1.setText = lambda x: self.Text1Var.set(x)
        self.Text1.text = lambda : self.Text1Var.get()
        self.Text1.place(relx=0.501, rely=0.041, relwidth=0.472, relheight=0.168)

        self.Text2Var = StringVar(value='')
        self.Text2 = Entry(self.top, textvariable=self.Text2Var, font=('宋体',10))
        self.Text2.setText = lambda x: self.Text2Var.set(x)
        self.Text2.text = lambda : self.Text2Var.get()
        self.Text2.place(relx=0.501, rely=0.325, relwidth=0.409, relheight=0.168)

        self.Path_buttonVar = StringVar(value='...')
        self.style.configure('TPath_button.TButton', font=('宋体',9))
        self.Path_button = Button(self.top, text='Command1', textvariable=self.Path_buttonVar, command=self.Path_button_Cmd, style='TPath_button.TButton')
        self.Path_button.setText = lambda x: self.Path_buttonVar.set(x)
        self.Path_button.text = lambda : self.Path_buttonVar.get()
        self.Path_button.place(relx=0.908, rely=0.325, relwidth=0.065, relheight=0.168)

        self.StartVar = StringVar(value='Start')
        self.style.configure('TStart.TButton', font=('宋体',14))
        self.Start = Button(self.top, text='Command2', textvariable=self.StartVar, command=self.Start_Cmd, style='TStart.TButton')
        self.Start.setText = lambda x: self.StartVar.set(x)
        self.Start.text = lambda : self.StartVar.get()
        self.Start.place(relx=0.016, rely=0.609, relwidth=0.472, relheight=0.249)

        self.QuitVar = StringVar(value='Quit')
        self.style.configure('TQuit.TButton', font=('宋体',14))
        self.Quit = Button(self.top, text='Command3', textvariable=self.QuitVar, command=self.Quit_Cmd, style='TQuit.TButton')
        self.Quit.setText = lambda x: self.QuitVar.set(x)
        self.Quit.text = lambda : self.QuitVar.get()
        self.Quit.place(relx=0.501, rely=0.609, relwidth=0.472, relheight=0.249)

class Application(Application_ui):。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def Path_button_Cmd(self, event=None):
        self.Text2Var.set(tkFileDialog.askdirectory())

    def Start_Cmd(self, event=None):
        main(self.Text1Var.get(),self.Text2Var.get())

    def Quit_Cmd(self, event=None):
        top.destroy()


class Solve():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Referer': 'https://music.163.com/'
        }


    def getid(self, list_id):  # 获取id
        url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id=' + list_id
        text = loads(get(url, headers=self.headers).text)  # 获取返回值
        idss = list(map(lambda x: str(x['id']), text['playlist']['trackIds']))
        ids = [str(x['id']) for x in text['playlist']['trackIds']]
        print(idss == ids)
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

def main(list_id,path):
    try:
        assert list_id
        assert path
        cool = Solve()
        ids, list_name = cool.getid(list_id)
        pool = Pool()
        os.chdir(path)
        if not os.path.exists(list_name):
            try:
                os.mkdir(list_name)
            except:
                list_name = '请自行修改文件夹名'
                os.mkdir(list_name)
        os.chdir(list_name)
        pool.map(cool.getdetail, ids)
        pool.close()
        pool.join()
    except AssertionError:
        showwarning('警告','请输入id或地址')
    

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()



