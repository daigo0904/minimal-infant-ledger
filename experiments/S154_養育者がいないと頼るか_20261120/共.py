import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S154B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S154世界', P + 'S154_養育者がいないと頼るか_20261120/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
V = L('S151v2', P + 'S151_損も見る食べ予測_20261120/v2.py'); 元換算 = B.換算; 包 = V.に(元換算, W, B)
構成 = {'元': dict(), 'v3': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満'), 'v4': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)}
def 一生(s, 参照, 名='元', 寿命=8000, 物知り=None):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False); V.設定.update(構成[名]); B.換算 = 包
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 9; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 参照=参照, 物知り=物知り)
    finally: B.換算 = 元換算; W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数える(o, lo, hi):
    """表情に従う差（良い顔の時に取る − 悪い顔の時に取る）を、養育者・物知り（赤ちゃん1）・ほかの仲間の前で。物知りの見ている子は 0,2..7（自分は見ない）。"""
    A, 相, 物 = o['行動列'][lo:hi], o['相手列'][lo:hi], o['物'][lo:hi]; 取 = A == 0; r = []
    for m in [相 == 0, 相 == 2, (相 > 0) & (相 != 2)]:
        r.append(float(取[m & (物 == 1)].mean() - 取[m & (物 == -1)].mean()))
    return tuple(r) + (float(o['食列'][lo:hi].mean()),)
