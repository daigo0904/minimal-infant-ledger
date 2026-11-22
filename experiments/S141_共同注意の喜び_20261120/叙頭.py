"""S125：一番の赤ちゃん（換算・Q 0.01・v時定数5000）＋食べ予測（窓3・kf）で叙述的指さしの世界。手8。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S141共通2', '../S141_共同注意の喜び_20261120/共通2.py')
A2 = L('S141足す2', '../S141_共同注意の喜び_20261120/足す2.py')
B, W, N = C.B, C.W, C.N
原換算 = B.換算; 食換算 = A2.換算に(原換算, W, B)
def 一生(s, 叙述, kf=0.0, 寿命=8000):
    A2.設定['窓'] = 3; A2.設定['kf'] = kf; B.換算 = 食換算
    W.学び率 = 0.01; B.v時定数 = 5000.0; K = 8; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 4; W.見た目次元 = 8 + K + 1 + K; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 食べた見える=True, 視線=True, 指さし=True, 叙述=叙述)
    finally: A2.設定['kf'] = 0.0; B.換算 = 原換算; W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def 指す(o, lo, hi):
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; return float((A[相 == 0] >= 4).mean()), float((A[相 > 0] >= 4).mean()), float(o['食列'][lo:hi].mean())
