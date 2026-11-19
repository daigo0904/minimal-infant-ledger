"""速い層を「出来事の記憶」（DND に近いもの）にする。
手ごとに直近 容量 個の出来事 (φ, 食べたか) を覚える（古いものから消える＝すばやく忘れる）。
選ぶ時、いまの場面 φ に似た出来事（内積の上位 k 個）の「食べたか」の平均を、その手の見込み D[a] にする。
score に kD·max(v食,0)·(D − D の平均) を足す（つながり・S81 の速い層と同じ物差し）。"""
import numpy as np
設定 = dict(kD=3.0, 容量=300, k=16)
def 作る(B, W):
    class 出来事(B.換算):
        def __init__(s, 種, i, 頭):
            super().__init__(種, i, 頭); n = W.感覚数 + 1; C = 設定['容量']
            s.鍵 = np.zeros((W.行動数, C, n)); s.値 = np.zeros((W.行動数, C)); s.数 = np.zeros(W.行動数, dtype=int)
        def 見込み(s, φ):
            D = np.zeros(W.行動数); x = φ / (np.linalg.norm(φ) + 1e-9)
            for a in range(W.行動数):
                m = min(s.数[a], 設定['容量'])
                if m == 0: continue
                sim = s.鍵[a, :m] @ x; k = min(設定['k'], m); idx = np.argpartition(-sim, k - 1)[:k]
                D[a] = s.値[a, idx].mean()
            return D
        def 選ぶ(s, φ):
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            D = s.見込み(φ)
            score = q + B.c * max(s.v食, 0.0) * u * ê + 設定['kD'] * max(s.v食, 0.0) * (D - D.mean())
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            j = s.数[a] % 設定['容量']; s.鍵[a, j] = φ / (np.linalg.norm(φ) + 1e-9); s.値[a, j] = 1.0 if 食べた else 0.0; s.数[a] += 1
            return super().受ける(φ, a, q, e, 食べた, 我慢)
    return 出来事
