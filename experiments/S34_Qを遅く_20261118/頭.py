import sys, numpy as np
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
def 一生(s, 学び率, 寿命=8000):
    W.学び率 = 学び率
    try: return B.一生(s, 'その手だけ', 寿命)
    finally: W.学び率 = 0.05
def one(job):
    s, lr = job; o = 一生(s, lr)
    return (s, lr, B.区(o, 0, 500), [float(np.mean([B.区(o, 7000, 7500)[j], B.区(o, 7500, 8000)[j]])) for j in range(3)], float(o['h列'][70:80].mean()))
