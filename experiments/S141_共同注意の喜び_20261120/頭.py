"""S104：子.多数個 があればそれを使う（継ぐ世界）。
S103：多数の子（設定の番号の集まり）が None でなければ、その番号の子だけ多数に合わせる（入れ替わった子も同じ番号なので引き継ぐ）。
S100：多数=True なら、寄せる先を「見た手」ではなく「これまで見た手の速い頻度（α多数）の一番多い手」にする（同調伝達）。
S99 写す頭：換算型に「見た手と同じ手をすると褒められるか」を手に依らず1つで覚える予測を足す。
同.予測(φ)＝見た手と同じ手をした時の評価、違.予測(φ)＝違う手をした時の評価（どちらも相手の見た目から）。
選ぶ：score[見た手] += kM·(同 − 違)。見た手が無い（養育者）なら足さない。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W = P.B, P.W
設定 = dict(kM=0.0, 多数=False, α多数=0.02, 多数の子=None)
class 写す(B.換算):
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); n = len(s.Q[0]); s.同 = W.RLS(n); s.違 = W.RLS(n); s.見た手 = None; s.前見た = None; s.見た頻度 = np.zeros(W.行動数); s.番号 = i
    def 選ぶ(s, φ):
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + B.c * max(s.v食, 0.0) * u * ê
        s.前見た = s.見た手
        if s.見た手 is not None: s.見た頻度 += 設定['α多数'] * (np.eye(W.行動数)[s.見た手] - s.見た頻度)
        多 = s.多数個 if hasattr(s, '多数個') else (設定['多数'] if 設定['多数の子'] is None else (s.番号 in 設定['多数の子']))   # S104：子ごとの頭
        先 = (int(np.argmax(s.見た頻度)) if 多 else s.見た手) if s.見た手 is not None else None
        if 先 is not None and 設定['kM'] != 0.0: score[先] += 設定['kM'] * (s.同.予測(φ) - s.違.予測(φ))
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        if s.前見た is not None: (s.同 if a == s.前見た else s.違).学ぶ(φ, e)
        return super().受ける(φ, a, q, e, 食べた, 我慢)
