"""S99 写す頭：換算型に「見た手と同じ手をすると褒められるか」を手に依らず1つで覚える予測を足す。
同.予測(φ)＝見た手と同じ手をした時の評価、違.予測(φ)＝違う手をした時の評価（どちらも相手の見た目から）。
選ぶ：score[見た手] += kM·(同 − 違)。見た手が無い（養育者）なら足さない。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W = P.B, P.W
設定 = dict(kM=0.0)
class 写す(B.換算):
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); n = len(s.Q[0]); s.同 = W.RLS(n); s.違 = W.RLS(n); s.見た手 = None; s.前見た = None
    def 選ぶ(s, φ):
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + B.c * max(s.v食, 0.0) * u * ê
        s.前見た = s.見た手
        if s.見た手 is not None and 設定['kM'] != 0.0: score[s.見た手] += 設定['kM'] * (s.同.予測(φ) - s.違.予測(φ))
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        if s.前見た is not None: (s.同 if a == s.前見た else s.違).学ぶ(φ, e)
        return super().受ける(φ, a, q, e, 食べた, 我慢)
