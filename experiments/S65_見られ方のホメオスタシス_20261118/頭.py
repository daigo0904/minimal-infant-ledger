import sys, numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S64R', '../S64_構われないと_20261118/走らせる.py')
B, W, N = M.B, M.W, M.N
設定 = dict(目標=0.3, k=1.0, 時定数=50.0, 目安=0.05)
class 恒常(B.換算):
    """見られ方のホメオスタシス：s＝大事な相手（つながり u>0）から受けた評価の漏れる和。
    報酬 = −h² − k·max(0, 目標−s)²。不足 d=max(0,目標−s) を Q の入力に1つ足す（d で手の値打ちを変えられるように）"""
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); s.Q = np.zeros((W.行動数, W.感覚数 + 2)); s.s = 0.0; s.拡 = None
    def 不足(s): return max(0.0, 設定['目標'] - s.s)
    def 選ぶ(s, φ):
        s.拡 = np.append(φ, s.不足()); q = s.Q @ s.拡
        ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + B.c * max(s.v食, 0.0) * u * ê
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        cu = float(np.clip(s.つながり.予測(φ) / 設定['目安'], 0, 1))
        s.s += (cu * e - s.s) / 設定['時定数']
        拡 = s.拡
        super().受ける(φ, a, q, e, 食べた, 我慢)
        s.前 = (拡, a, -s.h ** 2 - 設定['k'] * s.不足() ** 2)
def 一生(種, 腕, 欠乏, 寿命=8000, 記録=None):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = 恒常 if 腕 == 'あり' else B.換算
    try: return N.一生(種, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def 数(o): return (M.P養(o, 7500, 7700), M.B.区(o, 7000, 7500)[2])
