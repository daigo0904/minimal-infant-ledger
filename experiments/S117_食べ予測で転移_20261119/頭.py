"""S117：S116 の頭を S110 の世界（視線切替あり）で使う写し。
S116 食べの予測つきの頭：換算型に、手ごとの「この手の直後に食べたか」の予測 f̂[a]（RLS・ê と同じ形）を足す。
選ぶ：score = 換算型の score + kf·(f̂ − f̂ の平均)。kf=0 なら換算型と同じ手になる。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S110共通2', '../S110_視線追いの転移_20261119/共通2.py')
B, W = C.B, C.W
設定 = dict(kf=0.0)
class 食べ予測(B.換算):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); n = len(s.Q[0]); s.食 = [W.RLS(n) for _ in range(W.行動数)]
    def 選ぶ(s, φ):
        if 設定['kf'] == 0.0: return super().選ぶ(φ)
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ); f = np.array([m.予測(φ) for m in s.食])
        score = q + B.c * max(s.v食, 0.0) * u * ê + 設定['kf'] * (f - f.mean())
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        s.食[a].学ぶ(φ, 1.0 if 食べた else 0.0); return super().受ける(φ, a, q, e, 食べた, 我慢)
def 一生(s, kf, 腕='本物', 寿命=8000, **kw):
    設定['kf'] = kf; 原 = B.換算; B.換算 = 食べ予測
    try: return C.一生(s, 4, 腕, 寿命=寿命, 学び率=0.01, **kw)
    finally: B.換算 = 原; 設定['kf'] = 0.0
def 持ち上がり(o, lo, hi, 相手=0):
    A, 相, 視 = o['行動列'], o['相手列'], o['視線列']; 好 = np.array(o['好み']); 順 = np.argsort(好); 端 = {int(順[0]), int(順[-1])}; 上 = {True: [], False: []}
    for i in range(8):
        sel = (相[lo:hi, i] == 0) if 相手 == 0 else (相[lo:hi, i] > 0)
        m = np.arange(lo, hi)[sel]; g = 視[m, 0] if 相手 == 0 else 視[m, 相[m, i]]; a = A[m, i]
        for x in range(4):
            if (g == x).any() and (g != x).any(): 上[x in 端].append((a[g == x] == x).mean() - (a[g != x] == x).mean())
    return float(np.mean(上[True])), float(np.mean(上[False]))
