import sys, numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S65頭', '../S65_見られ方のホメオスタシス_20261118/頭.py')
B, W, N, M = H.B, H.W, H.N, H.M
H.設定.update(目標=0.3, k=1.0)
g = [3.0]
class 強まる(H.恒常):
    """S65 の恒常に、選ぶ時のつながりの項へ (1 + g·不足) を掛ける（欠乏がその場で欲求を強める）"""
    def 選ぶ(s, φ):
        s.拡 = np.append(φ, s.不足()); q = s.Q @ s.拡
        ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + (1 + g[0] * s.不足()) * B.c * max(s.v食, 0.0) * u * ê
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
def 一生(種, gg, 欠乏, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; g[0] = gg; N.赤ちゃん = 強まる
    try: return N.一生(種, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def 数(o, 欠乏): return (M.P養(o, 7500, 7700), None if 欠乏 else M.B.区(o, 7000, 7500)[2])
