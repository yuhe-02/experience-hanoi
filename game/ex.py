import tkinter as tk
from tkinter import font
import pandas as pd

class Hanoilog:
    def __init__(self,N):
        self.N = N
        self.ans = []
        self.towers = self.makeTowers(N)
        
    def makeTowers(self, n):
        '''ハノイの塔の初期配置を持つ辞書を作成する
        例えば，高さ3なら {'A':[3,2,1], 'B':[], 'C':[]} となる．
        各場所毎にどういう円盤があるかをリストで表現している．中身の数字が円盤を表している．
        リスト内では先頭の要素が山の一番下であり，最後の要素が山の一番上である．
        '''
        return {'A': list(range(n, 0, -1)), 'B': [], 'C': []}

    def move(self, f, t):
        '''fからtへ1枚円盤を移動させる'''
        s = f'move from {f} to {t}'
        # print(s)
        disk = self.towers[f][-1]
        self.ans.append([disk,f,t,len(self.towers[f]),len(self.towers[t])])
        self.towers[t].append(disk)
        self.towers[f].pop()
        # self.printT()  # 現在のtowersの状態を表示する

    def hanoi(self, n, begin, to, work):
        '''ハノイの塔のプログラムの本体．
        frm から to へ高さnumの山を移動させる．
        '''
        if n == 1:
            self.move(begin, to)  # 1枚ならそれを移動させるだけ．
        else:
            self.hanoi(n - 1, begin, work, to)
            self.move(begin, to)
            self.hanoi(n - 1, work, to, begin)

    def printT(self):
        '''towersの中身をうまく表示する．
        最初は単にprint(towers)としておけば良いかも．
        '''
        print(self.towers)
        
    def run(self):
        self.hanoi(self.N, 'A', 'C', 'B')
        df = pd.DataFrame(self.ans)
        df.columns = ["disk_num","from","to","from_num","to_num"]
        return df
