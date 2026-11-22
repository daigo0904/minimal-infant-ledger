import sys, numpy as np, importlib.util
sys.path.insert(0, '../S137_覚えた順番交代は保たれるか_20261119')
from 共 import *
G = L('S127重み', '../S127_癖の重み_20261119/重み.py'); 包 = G.に(B.換算, W, B); 原 = B.換算
def 一生λ(s, 番, λ, 寿命=8000):
    G.設定['λ'] = λ; B.換算 = 包
    try: return 一生(s, 番, 寿命)
    finally: B.換算 = 原; G.設定['λ'] = 1.0
