import sys, numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S64R', '../S64_構われないと_20261118/走らせる.py')
B, W, N = M.B, M.W, M.N
率 = dict(V=0.05, A=0.01)
class 分ける(B.換算):
    """癖を Q(a) = V·x + A[a]·x に分ける（x=[φ, h]）。δ はまず V（全部の手で共有）を学び、A[a] は小さく学ぶ。
    self.Q は常に A + V（換算型の δ・v食 の計算と選ぶはそのまま使える）。元の Q 更新は学び率 0 で止める"""
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); n = W.感覚数 + 2
        s.V = np.zeros(n); s.A = np.zeros((W.行動数, n)); s.Q = s.A + s.V; s.x = None
    def 選ぶ(s, φ):
        s.x = np.append(φ, s.h); q = s.Q @ s.x
        ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + B.c * max(s.v食, 0.0) * u * ê
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        前 = s.前; x = s.x
        lr = W.学び率; W.学び率 = 0.0
        try: super().受ける(φ, a, q, e, 食べた, 我慢)
        finally: W.学び率 = lr
        if 前 is not None:
            xp, ap, Rp = 前; δ = Rp + W.割引 * q[a] - s.Q[ap] @ xp; n2 = xp @ xp
            s.V += 率['V'] * δ * xp / n2; s.A[ap] += 率['A'] * δ * xp / n2; s.Q = s.A + s.V
        _, a2, R = s.前; s.前 = (x, a2, R)
def 一生(種, 腕, 欠乏, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = 分ける if 腕 == 'V+A' else B.換算
    try: return N.一生(種, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def 数(o, 欠乏): return (M.P養(o, 7500, 7700), None if 欠乏 else B.区(o, 7000, 7500)[2])
