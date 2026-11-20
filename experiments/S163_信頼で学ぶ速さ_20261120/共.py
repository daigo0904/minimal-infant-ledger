import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S163B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S163世界', P + 'S163_信頼で学ぶ速さ_20261120/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
V = L('S163v2', P + 'S163_信頼で学ぶ速さ_20261120/v2.py'); 元換算 = B.換算; 包 = V.に(元換算, W, B)
構成 = {'v4': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)}
皆 = []
class 記包(包):
    """S156：選ぶ前に中身を記録するだけ（乱数を使わない＝手は変わらない）。記録＝(取る手の余裕 score[0]−max(score[1:]), 食べ予測 f̂[0]−平均, λ·q[0]−平均)"""
    def __init__(s, *a):
        super().__init__(*a); s.記 = []; 皆.append(s)
    def 選ぶ(s, φ):
        S = V.設定; q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = S['λ'] * q + B.c * max(s.v食, 0.0) * u * ê; 重さ = float(np.clip(u / S['目安'], 0, 1))
        f = np.array([m.予測(φ) for m in s.食]); score = score + S['kf'] * (f - f.mean())
        score[int(np.argmax(ê))] += S['kD'] * max(s.遅_ - s.速_, 0.0) * 重さ
        s.記.append((float(score[0] - score[1:].max()), float(f[0] - f.mean()), float(S['λ'] * (q[0] - q.mean()))))
        return super().選ぶ(φ)
def 一生(s, 参照, 名='v4', 寿命=8000, 物知り=None, 記録=False, 合図2=None, kτ=0.0, 物知り率=None, 信型='外れ', 学型=None, 効き目=True):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False, kτ=kτ, 信型=信型, 学型=学型, 効き目=効き目); V.設定.update(構成[名]); B.換算 = 記包 if 記録 else 包
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 9 if 合図2 is None else 10; N.赤ちゃん = B.換算; 皆.clear()
    try:
        o = N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 参照=参照, 物知り=物知り, 合図2=合図2, 物知り率=物知り率)
        if 記録: o['記'] = np.array([c.記 for c in 皆]).transpose(1, 0, 2)   # [手, 子, 3]
        return o
    finally: B.換算 = 元換算; W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 顔(s, 寿命, 物知り):
    物 = np.where(np.random.default_rng([s, 16]).random((寿命, 8)) < 0.5, 1, -1); うそ = np.random.default_rng([s, 19]).random((寿命, 8))
    return 物, 物 * np.where(うそ < 物知り[1], 1, -1)
def 数える(o, s, 物知り, lo=6000, hi=8000):
    """物知りの前（相==2）で：正体ごとの取る差／顔ごとの取る差／顔ごとの 余裕・f̂・q の差。"""
    物, 顔の = 顔(s, len(o['行動列']), 物知り); assert (物 == o['物']).all()
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; 物, 顔の = 物[lo:hi], 顔の[lo:hi]; 取 = (A == 0).astype(float); m = 相 == 2
    d = lambda x, k: float(x[m & (k == 1)].mean() - x[m & (k == -1)].mean())
    r = [d(取, 物), d(取, 顔の)]
    if '記' in o:
        R = o['記'][lo:hi]; r += [d(R[:, :, j], 顔の) for j in range(3)]
    return tuple(r)
def 合図2の差(o, s, 合図2, lo, hi, 相の値=2):
    """後半：相手（既定＝物知り）の前で、2つ目の合図が +1 の時に取る − −1 の時に取る。"""
    T = len(o['行動列']); 物 = o['物']; うそ2 = np.random.default_rng([s, 21]).random((T, 8)); でた2 = np.where(np.random.default_rng([s, 22]).random((T, 8)) < 0.5, 1, -1)
    合 = np.where(o['相手列'] == 2, 物 * np.where(うそ2 < 合図2[1], 1, -1), でた2)
    A, 相, 合 = o['行動列'][lo:hi], o['相手列'][lo:hi], 合[lo:hi]; 取 = (A == 0).astype(float); m = 相 == 相の値
    return float(取[m & (合 == 1)].mean() - 取[m & (合 == -1)].mean())
