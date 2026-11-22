"""前の章の頭に「食べの予測 f̂[a]」（手ごとの RLS・その手の直後に食べたか）を足す。選び方は元のコードを写して kf·(f̂−平均) を足しただけ。kf=0 なら元と同じ手。"""
import numpy as np
設定 = dict(kf=0.0)
def 換算に(基, W, B):   # S30 の換算型の選ぶ（ずらしも選ぶは同じ）
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); n = len(s.Q[0]); s.食 = [W.RLS(n) for _ in range(W.行動数)]
        def 選ぶ(s, φ):
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = q + B.c * max(s.v食, 0.0) * u * ê
            if 設定['kf'] != 0.0: f = np.array([m.予測(φ) for m in s.食]); score = score + 設定['kf'] * (f - f.mean())
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            s.食[a].学ぶ(φ, 1.0 if 食べた else 0.0); return super().受ける(φ, a, q, e, 食べた, 我慢)
    return K
def 写すに(基, W, B, H設定):   # S100 の写す頭の選ぶ
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); n = len(s.Q[0]); s.食 = [W.RLS(n) for _ in range(W.行動数)]
        def 選ぶ(s, φ):
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = q + B.c * max(s.v食, 0.0) * u * ê
            s.前見た = s.見た手
            if s.見た手 is not None: s.見た頻度 += H設定['α多数'] * (np.eye(W.行動数)[s.見た手] - s.見た頻度)
            先 = (int(np.argmax(s.見た頻度)) if H設定['多数'] else s.見た手) if s.見た手 is not None else None
            if 先 is not None and H設定['kM'] != 0.0: score[先] += H設定['kM'] * (s.同.予測(φ) - s.違.予測(φ))
            if 設定['kf'] != 0.0: f = np.array([m.予測(φ) for m in s.食]); score = score + 設定['kf'] * (f - f.mean())
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            s.食[a].学ぶ(φ, 1.0 if 食べた else 0.0); return super().受ける(φ, a, q, e, 食べた, 我慢)
    return K
