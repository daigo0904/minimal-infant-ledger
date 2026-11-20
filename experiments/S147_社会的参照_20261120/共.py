import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S147B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S147世界', P + 'S147_社会的参照_20261120/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
V = L('S142v2', P + 'S142_空腹で切り替える_20261120/v2.py'); 元換算 = B.換算; 包 = V.に(元換算, W, B)
構成 = {'元': dict(), 'v3': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満')}
def 一生(s, 参照, 名='元', 寿命=8000):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None); V.設定.update(構成[名]); B.換算 = 包
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 9; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 参照=参照)
    finally: B.換算 = 元換算; W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数える(o, lo, hi):
    A, 相, 物, でた = o['行動列'][lo:hi], o['相手列'][lo:hi], o['物'][lo:hi], o['でた'][lo:hi]; 取 = A == 0; 養, 仲 = 相 == 0, 相 > 0
    表養 = 物  # 養育者の表情は（参照='養育者' なら）物
    return float(取[養 & (物 == 1)].mean() - 取[養 & (物 == -1)].mean()), float(取[仲 & (でた == 1)].mean() - 取[仲 & (でた == -1)].mean()), float(取[仲 & (物 == 1)].mean() - 取[仲 & (物 == -1)].mean()), float(o['食列'][lo:hi].mean())
