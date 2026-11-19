"""換算型の選びで癖（Q）の重みを λ にする：score = λ·q + c·max(v食,0)·u·ê。λ=1 なら元と同じ手。学びは変えない。"""
import numpy as np
設定 = dict(λ=1.0)
def に(基, W, B):
    class K(基):
        def 選ぶ(s, φ):
            if 設定['λ'] == 1.0: return super().選ぶ(φ)
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = 設定['λ'] * q + B.c * max(s.v食, 0.0) * u * ê; a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
    return K
