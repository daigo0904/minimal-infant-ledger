"""S191：S190 の世界・頭をそのまま読む。お返し：子 i が子 j になぐさめられてから 窓 手の間（恩あり）に j に見られた手で i が手3 をする割合 と、
そうでない時（恩なし）に j に見られた手で i が手3 をする割合（同じ相手 j どうしで比べる）。全部の組を合わせて数える。"""
import sys, numpy as np
sys.path.insert(0, '../S190_なぐさめの代価_20261121')
from 共 import 一生
def お返し(o, lo, hi, 窓=100):
    A, 相 = o['行動列'], o['相手列']; n = A.shape[1]; 恩 = np.full((n, n), -10**9)   # 恩[i, j]＝j が i をなぐさめた最後の手
    数 = np.zeros((2, 2))   # [恩あり/なし][手3の数, 見られた数]
    for t in range(hi):
        if t >= lo:
            for i in range(n):
                k = 相[t, i]
                if 0 < k <= n:
                    j = k - 1; あり = 0 if t - 恩[i, j] <= 窓 else 1; 数[あり, 0] += A[t, i] == 3; 数[あり, 1] += 1
        for j in range(n):
            k = 相[t, j]
            if 0 < k <= n and A[t, j] == 3: 恩[k - 1, j] = t   # j が (k−1) をなぐさめた
    a, b = 数[0, 0] / max(数[0, 1], 1), 数[1, 0] / max(数[1, 1], 1)
    return float(a - b), float(a), float(b), float(数[0, 1])
def 測る(s, kE=50.0, 窓=100):
    o = 一生(s, 'v4', なぐさめ=True, kE=kE, 共感型='苦しさ', 泣き=0.01, 代価=0.03); return お返し(o, 6000, 8000, 窓) + (o['sha256'],)
