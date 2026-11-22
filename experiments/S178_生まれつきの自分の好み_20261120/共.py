"""S175：S47 の『本物』と同じ設定（S30 の換算型・学び率0.01・v時定数5000・その手だけ）で、世界を S175 の写しに、頭を S151 の v2（v4）に。"""
import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S178B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S178世界', P + 'S178_生まれつきの自分の好み_20261120/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
V = L('S178v2', P + 'S178_生まれつきの自分の好み_20261120/v2.py'); 包 = V.に(B.換算, W, B)
構成 = {'元': dict(), 'v4': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)}
def 一生(s, 名='元', 寿命=8000, 二人=None, B同じ=False, 自分=None, k生まれ=0.0):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False, k生まれ=k生まれ); V.設定.update(構成[名])
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = 包
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 二人=二人, B同じ=B同じ, 自分=自分)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def 分け(o, lo, hi):
    """人ごとの見られ分け：A の前で A好き手の割合 − B の前で A好き手の割合、と B好き手の逆向き、の平均（子の平均）。"""
    A, 相, a1, b1 = o['行動列'][lo:hi], o['相手列'][lo:hi], o['一番'], o['一番B']; r = []
    for i in range(A.shape[1]):
        x, w = A[:, i], 相[:, i]; pA = np.bincount(x[w == 0], minlength=4) / max(1, (w == 0).sum()); pB = np.bincount(x[w == 9], minlength=4) / max(1, (w == 9).sum())
        r.append(((pA[a1] - pB[a1]) + (pB[b1] - pA[b1])) / 2)
    return float(np.mean(r))
def ブロッコリー(o, lo, hi):
    """子の平均：B の前で B好き手 − 自分好き手、仲間の前の 自分好き手の割合、A の前で A好き手 − 自分好き手。"""
    A, 相, a1, b1, 自 = o['行動列'][lo:hi], o['相手列'][lo:hi], o['一番'], o['一番B'], o['自分手']; r = []
    for i in range(A.shape[1]):
        x, w = A[:, i], 相[:, i]; p = lambda m: np.bincount(x[m], minlength=4) / max(1, m.sum()); pB, pA, pO = p(w == 9), p(w == 0), p((w > 0) & (w < 9))
        r.append((pB[b1] - pB[自[i]], pO[自[i]], pA[a1] - pA[自[i]]))
    return tuple(float(v) for v in np.mean(r, 0))
