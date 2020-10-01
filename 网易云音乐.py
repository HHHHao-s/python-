#!/usr/bin/env python
# -*- coding:utf-8 -*-
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
# import tkinter.simpledialog as tkSimpleDialog    #askstring()


class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Form1')
        self.master.geometry('722x334')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('TFrame1.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame1.TLabelframe.Label', font=('宋体', 9))
        self.Frame1 = LabelFrame(
            self.top, text='', style='TFrame1.TLabelframe')
        self.Frame1.place(relx=0.709, rely=0., relwidth=0.289, relheight=0.985)

        self.style.configure('TFrame2.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame2.TLabelframe.Label', font=('宋体', 9))
        self.Frame2 = LabelFrame(
            self.top, text='', style='TFrame2.TLabelframe')
        self.Frame2.place(relx=0.011, rely=0., relwidth=0.677, relheight=0.985)

        self.List1Var = StringVar(value='')
        self.List1Font = Font(font=('宋体', 9))
        self.List1 = Listbox(
            self.Frame1, listvariable=self.List1Var, font=self.List1Font)
        self.List1.place(relx=0.038, rely=0.049,
                         relwidth=0.923, relheight=0.924)

        self.IDVar = StringVar(value='歌单ID:')
        self.style.configure('TID.TLabel', anchor='w', font=('宋体', 9))
        self.ID = Label(self.Frame2, text='Label1',
                        textvariable=self.IDVar, style='TID.TLabel')
        self.ID.setText = lambda x: self.IDVar.set(x)
        self.ID.text = lambda: self.IDVar.get()
        self.ID.place(relx=0.016, rely=0.05, relwidth=0.46, relheight=0.128)

        self.PathVar = StringVar(value='下载地址')
        self.style.configure('TPath.TLabel', anchor='w', font=('宋体', 9))
        self.Path = Label(self.Frame2, text='Label2',
                          textvariable=self.PathVar, style='TPath.TLabel')
        self.Path.setText = lambda x: self.PathVar.set(x)
        self.Path.text = lambda: self.PathVar.get()
        self.Path.place(relx=0.016, rely=0.399, relwidth=0.46, relheight=0.128)
        self.Path.bind('<Button-1>', self.Path_Button_1)

        self.Text1Var = StringVar(value='')
        self.Text1 = Entry(
            self.Frame2, textvariable=self.Text1Var, font=('宋体', 9))
        self.Text1.setText = lambda x: self.Text1Var.set(x)
        self.Text1.text = lambda: self.Text1Var.get()
        self.Text1.place(relx=0.507, rely=0.05,
                         relwidth=0.476, relheight=0.128)

        self.Text2Var = StringVar(value='')
        self.Text2 = Entry(
            self.Frame2, textvariable=self.Text2Var, font=('宋体', 9))
        self.Text2.setText = lambda x: self.Text2Var.set(x)
        self.Text2.text = lambda: self.Text2Var.get()
        self.Text2.place(relx=0.507, rely=0.399,
                         relwidth=0.411, relheight=0.128)

        self.Path_buttonVar = StringVar(value='...')
        self.style.configure('TPath_button.TButton', font=('宋体', 9))
        self.Path_button = Button(self.Frame2, text='Command1', textvariable=self.Path_buttonVar,
                                  command=self.Path_button_Cmd, style='TPath_button.TButton')
        self.Path_button.setText = lambda x: self.Path_buttonVar.set(x)
        self.Path_button.text = lambda: self.Path_buttonVar.get()
        self.Path_button.place(relx=0.916, rely=0.399,
                               relwidth=0.067, relheight=0.128)

        self.StartVar = StringVar(value='Start')
        self.style.configure('TStart.TButton', font=('宋体', 9))
        self.Start = Button(self.Frame2, text='Command2', textvariable=self.StartVar,
                            command=self.Start_Cmd, style='TStart.TButton')
        self.Start.setText = lambda x: self.StartVar.set(x)
        self.Start.text = lambda: self.StartVar.get()
        self.Start.place(relx=0.016, rely=0.798,
                         relwidth=0.46, relheight=0.178)

        self.QuitVar = StringVar(value='Quit')
        self.style.configure('TQuit.TButton', font=('宋体', 9))
        self.Quit = Button(self.Frame2, text='Command3', textvariable=self.QuitVar,
                           command=self.Quit_Cmd, style='TQuit.TButton')
        self.Quit.setText = lambda x: self.QuitVar.set(x)
        self.Quit.text = lambda: self.QuitVar.get()
        self.Quit.place(relx=0.507, rely=0.798,
                        relwidth=0.476, relheight=0.178)


class Application(Application_ui):

    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def Path_Button_1(self, event):
        # TODO, Please finish the function here!
        pass

    def Path_button_Cmd(self, event=None):
        self.Text2Var.set(tkFileDialog.askdirectory())

    def Start_Cmd(self, event=None):
        main(self.Text1Var.get(), self.Text2Var.get())

    def Quit_Cmd(self, event=None):
        top.destroy()


class Solve():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Referer': 'https://music.163.com/'
        }
        self.n = 0
        self.new = ''

    def getid(self, list_id):  # 获取id
        url = 'https://api.imjad.cn/cloudmusic/?type=playlist&id=' + list_id
        text = loads(get(url, headers=self.headers).text)  # 获取返回值
        ids = [str(x['id']) for x in text['playlist']['trackIds']]
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
        print(name)
        f = open(path, 'wb')
        html = get(url, headers=self.headers, timeout=5)
        f.write(html.content)
        f.close()


def main(list_id, path):
    try:
        assert list_id
        assert path
        print(path, list_id)
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
        os.startfile(list_name)
        os.chdir(list_name) 
        pool.map(cool.getdetail, ids)
        pool.close()
        pool.join()
        print('完成')
    except AssertionError:
        showwarning('警告', '请输入id或地址')


if __name__ == "__main__":
    top = Tk()
    a = Application(top)
    a.mainloop()
