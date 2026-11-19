import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S = L('S123選び', '../S123_指す手柄_20261119/選び.py'); H, A2 = S.H, S.A2
def 一生(s, 効, kf=10.0, 寿命=8000):
    A2.設定['窓'] = 3; A2.設定['kf'] = kf
    try: return H.一生(s, kf, 効, 寿命=寿命)
    finally: A2.設定['kf'] = 0.0
def 数える(o, lo, hi):
    """養育者の前／仲間の前で、指す手（4〜7）の割合と当たりを指す割合。"""
    当 = o['当たり'][0] % 4; 相 = o['相手列'][lo:hi]; A = o['行動列'][lo:hi]; 養, 仲 = 相 == 0, 相 > 0
    return float((A[養] >= 4).mean()), float((A[仲] >= 4).mean()), float((A[養] == 4 + 当).mean()), float((A[仲] == 4 + 当).mean())
