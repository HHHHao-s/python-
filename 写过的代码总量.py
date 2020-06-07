import os
import easygui as e


class Solve:
    def __init__(self):
        self.line = 0
        print('将本文件放入要找的文件夹下即可')
    
    def find(self):
        for path,dirs,files in os.walk('.'):
            for file in files:
                if os.path.splitext(file)[1] == '.py':
                    with open(os.path.join(path,file),'r',encoding='utf-8') as f:
                        for a in f.readlines():
                            self.line += 1
        print(f"一共有.py文件{self.line}行")


def main():
    solve = Solve()
    solve.find()
    input()
main()

