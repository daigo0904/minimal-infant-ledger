"""調整用の種 900〜909：S64 の作りで λ=1／0.2、欠乏あり／なし。戻った直後 7500〜7700 の養育者が見ている手で、Q差・つながり差（一番の手 − 他の平均）、合計（λ·Q差＋つながり差）、P養。"""
import numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S64R', '../S64_構われないと_20261118/走らせる.py'); B, W, N = M.B, M.W, M.N
記録 = {}; 一番 = [0]; 設定 = dict(λ=1.0)
class 記す(B.換算):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; 記録[i] = []
    def 選ぶ(s, φ):
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ); Lk = B.c * max(s.v食, 0.0) * u * ê; b = 一番[0]
        score = 設定['λ'] * q + Lk
        記録[s.番].append((q[b] - np.delete(q, b).mean(), Lk[b] - np.delete(Lk, b).mean(), score[b] - np.delete(score, b).max()))
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
def 一番を調べる(s):
    世 = np.random.default_rng([s, 0]); return int(np.argmax(np.array(W.養育者の好み)[世.permutation(W.行動数)]))
def 一生(s, 欠乏, λ):
    W.学び率 = 0.01; B.v時定数 = 5000.0; 記録.clear(); 一番[0] = 一番を調べる(s); 設定['λ'] = λ; N.赤ちゃん = 記す
    try: return N.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; 設定['λ'] = 1.0
def one(job):
    s, 欠, λ = job; o = 一生(s, 欠, λ); R = np.array([記録[i] for i in range(8)]).transpose(1, 0, 2); m = o['相手列'][7500:7700] == 0; X = R[7500:7700][m]
    m0 = o['相手列'][6800:7000] == 0; X0 = R[6800:7000][m0]
    return [X[:, 0].mean(), X[:, 1].mean(), (λ * X[:, 0] + X[:, 1]).mean(), M.P養(o, 7500, 7700), X0[:, 1].mean(), float((X[:, 2] > 0).mean()), float(np.median(X[:, 2])), float(np.mean(X[:, 2][X[:, 2] < 0])) if (X[:, 2] < 0).any() else 0.0]
if __name__ == '__main__':
    with Pool(8) as p:
        for λ in [1.0, 0.2]:
            r = {e: np.array(p.map(one, [(s, e, λ) for s in range(900, 910)])) for e in [False, True]}
            for e in [False, True]:
                m = np.median(r[e], 0); print(f'λ={λ} 欠乏={e}: Q差 {m[0]:+.3f} つながり差 {m[1]:+.3f}（欠乏前 {m[4]:+.3f}） 合計 {m[2]:+.3f} P養 {m[3]:.3f}')
            for e in [False, True]:
                m = np.median(r[e], 0); print(f'      欠乏={e}: 一番の手が勝つ割合 {m[5]:.3f}  一番強いほかの手との差 中央値 {m[6]:+.3f}  負けている時の差 {m[7]:+.3f}')
            d = r[True] - r[False]; print(f'   欠乏−なし: Q差 {np.median(d[:,0]):+.3f} つながり差 {np.median(d[:,1]):+.3f} 合計 {np.median(d[:,2]):+.3f}（>0 {int((d[:,2]>0).sum())}/10） P養 {np.median(d[:,3]):+.3f}（>0 {int((d[:,3]>0).sum())}/10）')
