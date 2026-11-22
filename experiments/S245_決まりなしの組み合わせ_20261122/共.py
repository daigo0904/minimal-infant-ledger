"""S235：頭は S227〜S234 と同じ v4＋共感 kE50。世界は S235。"""
import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S245B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S245世界', P + 'S245_決まりなしの組み合わせ_20261122/世界.py')
V = L('S245v2', P + 'S245_決まりなしの組み合わせ_20261122/v2.py'); 包 = V.に(B.換算, W, B)
構成 = {'v4': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)}
def 点(子, φ):
    S = V.設定; q = 子.Q @ φ; f = np.array([m.予測(φ) for m in 子.食]); return S['λ'] * q + S['kf'] * (f - f.mean())
def 一生(s, 寿命=16000, kE=50.0, 話し方='ふつう', 未見まで=None, 聞き方='まとめて', kC=0.0):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False, kE=kE, kC=kC); V.設定.update(構成['v4'])
    W.学び率 = 0.01; B.v時定数 = 5000.0
    try: return N.一生(s, 包, W, 寿命=寿命, 話し方=話し方, 点=点, 未見まで=未見まで, 聞き方=聞き方)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
