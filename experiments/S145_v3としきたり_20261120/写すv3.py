"""S145：v3 の部品（S142 の v2.py）を S100 の多数に合わせる頭（写す）に足す。選びは v3 の score に、写す頭の上乗せ kM·(同−違) を見た手（多数なら見た頻度の一番）に足す。
v3 の部品が全部 0 なら写す頭の選ぶ（元）をそのまま使う。"""
import numpy as np
def 作る(V, H, W, B):
    基 = V.に(H.写す, W, B)
    class K(基):
        def 選ぶ(s, φ):
            S = V.設定
            if S['kf'] == 0.0 and S['kD'] == 0.0 and S['λ'] == 1.0: return super().選ぶ(φ)
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = S['λ'] * q + B.c * max(s.v食, 0.0) * u * ê
            if S['kf'] != 0.0: f = np.array([m.予測(φ) for m in s.食]); score = score + S['kf'] * (s.h if S['切替'] in ('f空', '両方') else 1.0) * (f - f.mean())
            if S['kD'] != 0.0: score[int(np.argmax(ê))] += S['kD'] * max(s.遅_ - s.速_, 0.0) * float(np.clip(u / S['目安'], 0, 1))
            # 写す頭の上乗せ（S100 の 頭.py と同じ）
            s.前見た = s.見た手
            if s.見た手 is not None: s.見た頻度 += H.設定['α多数'] * (np.eye(W.行動数)[s.見た手] - s.見た頻度)
            多 = H.設定['多数']
            先 = (int(np.argmax(s.見た頻度)) if 多 else s.見た手) if s.見た手 is not None else None
            if 先 is not None and H.設定['kM'] != 0.0: score[先] += H.設定['kM'] * (s.同.予測(φ) - s.違.予測(φ))
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
    K._v2 = True
    return K
