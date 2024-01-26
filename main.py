from game.user import UserMonit
"""
import tkinter as tk
from tkinter import font
import time
import sys
import pandas as pd
"""
if __name__ == "__main__":
    difficulty = ["easy","normal","hard"]
    N = int(input("ここに数値を入力してください："))
    diff = int(input("難易度 0:簡単,1:普通,2:難しい："))
    c = UserMonit(N=N,difficulty=difficulty[diff])
    c.main()