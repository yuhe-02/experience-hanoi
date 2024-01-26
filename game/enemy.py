import tkinter as tk
from tkinter import font
import pandas as pd
import time
from .ex import Hanoilog

class EnemyMonit:
    def __init__(self,N,difficulty):
        self.root = tk.Tk()
        self.root.title("EnemyWindow")
        self.root.geometry("600x300")
        self.canv = self.set_canv("white")
        self.canv2 = self.set_canv("blue")
        
        df = Hanoilog(N=N).run()
        self.disks = df["disk_num"]
        self.froms = df["from"]
        self.tos = df["to"]
        self.from_nums = df["from_num"]
        self.to_nums = df["to_num"]
        
        self.N = N
        self.center = 95
        self.top = 15
        self.count = 0
        self.set_counter()
        
        self.create_obj(self.N,self.top)
        self.flg = False
        self.speed = self.select_spped(difficulty)
    
    def select_spped(self,difficulty):
        if difficulty == "easy":
            return 0.1
        if difficulty == "normal":
            return 0.01
        if difficulty == "hard":
            return 0.001
        else:
            print("easy,normal,hardから選んでください。hardで始めます")
            return 0.001
    def set_counter(self):
        font1 = font.Font(family='Helvetica', size=200, weight='bold')
        label = tk.Label(self.canv2, text=f"試行回数：{self.count}",font=font1)
        label.place(x=0, y=40)
        return None
    
    def set_canv(self,color):
        canv = tk.Canvas(self.root, bg=color,width=600,height=150)
        canv.pack()
        return canv
    
    def steps(self):
        return len(self.disks)
    
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
    
    
    def get_shapes_with_tag(self):
        # 指定したタグに関連付けられた図形のIDを取得
        shape = self.canv.bbox("dragged")
        return shape
    
    def move(self,disk,fr,t,from_num,to_num):
        self.canv.addtag_withtag('dragged',disk)
        tagged_shapes = self.get_shapes_with_tag()
        length = (tagged_shapes[2]-tagged_shapes[0])//2
        achieve_height = 150 - 15*(to_num+1)
        
        if t == "A":
            center = 100
        if t == "B":
            center = 300
        if t == "C":
            center = 500  
        target_x = center - length
        target_y = achieve_height
        if self.canv.coords("dragged") == []:
            return 
        # print("working")
        self.canv.after(10, self.move_rect(target_x, target_y))
        self.canv.dtag('dragged','dragged')
        
    
    def move_rect(self,target_x,target_y):
        # 現在の円の座標を取得
        if self.canv.coords("dragged") == []:
            # print("finish")
            return
        (x, y, _, _) = self.canv.coords("dragged")
        while (x, y) != (target_x, target_y):
            (x, y, _, _) = self.canv.coords("dragged")
            # 移動先の座標に対して現在の座標が近づくように移動
            if x < target_x:
                self.canv.move("dragged", 1, 0)
            elif x > target_x:
                self.canv.move("dragged", -1, 0)

            if y < target_y:
                self.canv.move("dragged", 0, 1)
            elif y > target_y:
                self.canv.move("dragged", 0, -1)
            time.sleep(self.speed)
            self.root.update()
    
    def main(self):
        self.root.after(1, self.execute_steps())
        return time.time()
        self.root.mainloop()

    def execute_steps(self):
        for i in range(len(self.disks)):
            disk = self.disks[i]
            fr = self.froms[i]
            t = self.tos[i]
            from_num = self.from_nums[i]
            to_num = self.to_nums[i]
            self.move(disk, fr, t, from_num, to_num)
            self.root.after(0, lambda: None)
            self.count += 1
            self.set_counter()
        
    

# if __name__ == "__main__":
#     c = EnemyMonit(10)
#     c.main()