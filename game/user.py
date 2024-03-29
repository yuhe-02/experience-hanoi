import tkinter as tk
from tkinter import font
import time
from .enemy import EnemyMonit
import sys
import PySimpleGUI as sg

class UserMonit:
    def __init__(self,N,difficulty):
        self.root = tk.Tk()
        self.root.title("UserWindow")
        self.root.geometry("600x300")
        self.canv = self.set_canv("white")
        self.canv2 = self.set_canv("blue")
        
        self.N = N
        self.center = 95
        self.top = 15
        self.count = 0
        self.set_counter()
        
        self.create_obj(self.N,self.top)
        self.button = self.clr_btn("クリア判定",5,5)
        self.button2 = self.str_btn("スタート",150,5)
        self.e = EnemyMonit(N=self.N,difficulty=difficulty)
        self.steps = self.e.steps()
        self.start = 0
        self.cpu_end = 0
        self.label = None
    
    def set_counter(self):
        font1 = font.Font(family='Helvetica', size=20, weight='bold')
        label = tk.Label(self.canv2, text=f"試行回数：{self.count}",font=font1)
        label.place(x=0, y=40)
        return None
    
    def set_canv(self,color):
        canv = tk.Canvas(self.root, bg=color,width=600,height=150)
        canv.pack()
        return canv
        
    def clr_btn(self,text,x,y,condition=False):
        button = tk.Button(self.canv2, text=text, command=lambda: self.clr_button_click())
        if not condition:
            button.config(state=tk.DISABLED)
        button.pack()
        button.grid(row=0, column=0)
        button.place(x=x, y=y)
        return button
    
    def str_btn(self,text,x,y):
        button = tk.Button(self.canv2, text=text, command=lambda: self.str_button_click())
        button.pack()
        button.grid(row=0, column=0)
        button.place(x=x, y=y)
        return button
    
    def create_obj(self,N,top):
        height_by_allobjects = N*top
        dic = {0:"green",1:"black",2:"blue",3:"red",4:"yellow",5:"red"}
        for i in range(N):
            self.canv.create_rectangle(25-5*i,
                                       (150-height_by_allobjects)+15*i,
                                       175+5*i,
                                       (150-height_by_allobjects)+15*(i+1),
                                       tag=f'{i+1}',
                                       fill=dic[i%6])

    def mousePressed(self,event):
        global coord
        global px,py  # px,pyをグローバル変数として宣言して，他の関数からもアクセスできるようにする．
        x,y = event.x,event.y
        target_list,_ = self.find_obj_num(event,x)
        
        coord = self.memorize_coord(target_list) #動かそうとしているオブジェクトの元の座標を記憶している
        # event.widget.addtag_overlapping('dragged',x,y,x,y)  # マウスボタンが押された場所にある図形にタグをつける．
        event.widget.addtag_withtag('dragged',min(target_list))
        px,py = x,y  # マウスボタンが押された位置を記憶しておき，次のイベント発生時にどれだけ移動したか計算できるように準備する．
        
    def mouseDragged(self,event):
        global dragobj
        global px,py
        dragobj = int(event.widget.gettags(event.widget.find_withtag(tk.CURRENT))[0]) #動かしているオブジェクトのサイズが何番目に大きいか記憶する
        event.widget.move('dragged',event.x-px,event.y-py)  # 前回のイベント発生時のカーソル位置と現在の位置との差を計算して，その分だけ図形を移動させる．
        px,py = event.x,event.y                             # 今回のイベント発生位置（カーソル位置）を記録しておく．

    def mouseReleased(self,event):
        self.set_button_condition(event)   
                
        center = (self.canv.coords("dragged")[2]+self.canv.coords("dragged")[0])//2
        target_list,start_position = self.find_obj_num(event,center)
        self.judge_and_place_obj(target_list,start_position)
        event.widget.dtag('dragged','dragged') 
    
    def set_button_condition(self,event):
        if len(event.widget.find_overlapping(401,0,600,150)) == self.N:
            self.button.config(state=tk.NORMAL)
        else:
            self.button.config(state=tk.DISABLED)
            
    def memorize_coord(self,target_list):
        # example :coordinate = (0,0,15,15)F
        item_id = min(target_list)
        coordinate = self.canv.coords(item_id)
        
        return coordinate
    
    def judge_and_place_obj(self,target_list,start_position):
        length = self.canv.coords("dragged")[2]-self.canv.coords("dragged")[0]
        mini = int(min(target_list)) #配置したい場所のオブジェクトを探索し、その中で最も小さいオブジェクトを見つける
        target_num = len(target_list) #配置したい場所にあるオブジェクトの数を算出する
        if mini < dragobj:
            self.canv.coords('dragged', coord[0], coord[1], coord[2], coord[3])
        else:
            self.canv.coords('dragged', start_position-(length//2), 135-15*(target_num-1), start_position+(length//2), 150-15*(target_num-1))

            self.count += 1
            self.set_counter()
    
    def find_obj_num(self,event,center):
        if center > 0 and center <= 200:
            target_list = event.widget.find_overlapping(1,0,200,150)
            start_position = 100

        elif center > 200 and center <= 400:
            target_list = event.widget.find_overlapping(201,0,400,150)
            start_position = 300
            
        elif center > 400 and center <= 600:
            target_list = event.widget.find_overlapping(401,0,600,150)
            start_position = 500
        return target_list,start_position
    
    def clr_button_click(self):
        usr_end = time.time()
        
        message1 = f"クリア！！あなたの試行回数:{self.count}回, CPUの試行回数:{self.steps}回"
        if self.cpu_end == 0:
            message2 = f"あなたの勝ち！試行時間:{round(usr_end-self.start,1)}"
        else:
            message2 = f"あなたの試行時間:{round(usr_end-self.start,1)}, CPUの試行時間:{round(self.cpu_end-self.start,1)}"
        self.result_monit(message1,message2)
        
        self.e.close_window()
        self.root.destroy()
        sys.exit()
        

    def str_button_click(self):
        self.button2.config(state=tk.DISABLED)
        self.start_battle()
        return
    
    def start_battle(self):
        START_COUNT = 5
        font1 = font.Font(family='Helvetica', size=30, weight='bold')
        self.label = tk.Label(self.canv, text=f"{START_COUNT}",font=font1)
        self.label.place(x=100, y=50)    
        self.countdown(START_COUNT)
        self.flg = True

    def countdown(self, counter):
        if counter > 0:
            self.label.config(text=f'{counter}')
            k = self.root.after(1000, self.countdown, counter-1)  # 1秒後にcountdown()を再帰的に呼び出す
            return 
        else:
            # self.label.config(text='START!!!')
            self.label.destroy()
            self.start = time.time()
            self.cpu_end = self.e.main()
            return True
        
    def result_monit(self,message1,message2):
        layout = [[sg.Text(f"{message1}\n{message2}")], [sg.Button("OK")]]

        window = sg.Window("結果画面", layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "OK":
                break

        window.close()
    
    def main(self):
        self.canv.bind('<Button-1>', self.mousePressed)          # ボタンが押されたときのコールバック設定
        self.canv.bind('<B1-Motion>', self.mouseDragged)         # ドラッギング中のコールバック設定
        self.canv.bind('<ButtonRelease-1>', self.mouseReleased)
        self.root.mainloop()
