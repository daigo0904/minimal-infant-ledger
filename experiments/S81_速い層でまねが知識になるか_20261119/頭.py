"""2層の赤ちゃん：遅い癖（Q）＋速い層（いま効く手の短い覚え）。
速い層 F[a]：手 a をした直後に食べられたか（1/0）のすばやい平均（α）。相手や場面に依らない「いまこの手は効く」。
選ぶ：score = q + つながり項 + kF·max(v食,0)·(F − F の平均)（一食の値打ちで換算＝つながりと同じ物差し）"""
import sys, numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S80R', '../S80_まねが広がるか_20261119/走らせる.py')
B, W, N = P.B, P.W, P.N
設定 = dict(kF=10.0, α=0.1)
class 二層(B.換算):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.F = np.zeros(W.行動数)
    def 選ぶ(s, φ):
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + B.c * max(s.v食, 0.0) * u * ê + 設定['kF'] * max(s.v食, 0.0) * (s.F - s.F.mean())
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        s.F[a] += 設定['α'] * ((1.0 if 食べた else 0.0) - s.F[a])
        return super().受ける(φ, a, q, e, 食べた, 我慢)
def 一生(s, 層, 手本頻度=1 / 7, 寿命=8000, 手本=True):
    W.学び率 = 0.05; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = 二層 if 層 else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=手本, お手本の頻度=手本頻度)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数(o):
    A, 相, 当 = o['行動列'], o['相手列'], np.array(o['当たり']); 当t = 当[np.arange(len(A)) // 1000]
    乗 = float(np.mean([(A[c:c + 500, 1:] == 当[c // 1000]).mean() for c in range(2000, 8000, 1000)]))
    他 = P.数(o); 手 = []
    for i in range(1, 8):
        m = 相[:, i] == 1; 手.append((A[m, i] == 当t[m]).mean())
    return 乗, 他, float(np.mean(手))
