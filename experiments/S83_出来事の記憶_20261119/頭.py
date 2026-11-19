import sys, numpy as np, importlib.util
sys.path.insert(0, '../S83_出来事の記憶_20261119')
import 記憶
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
T = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W, N = T.B, T.W, T.N
出来事 = 記憶.作る(B, W)
def 一生(s, 層, 手本=True, 寿命=8000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = 出来事 if 層 else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=手本, お手本の頻度=1 / 7)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
数 = T.数
