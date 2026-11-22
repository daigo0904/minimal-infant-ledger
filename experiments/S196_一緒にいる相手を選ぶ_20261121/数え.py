"""S194：S193 の世界・頭をそのまま読む。i が j に見られた手のうち i が手3 をした割合 R[i,j]（会う回数の差を消す）から、
(1) 組のそろい方＝R[i,j] と R[j,i] の相関（28組）、(2) なぐさめ先の偏り＝各子の R の上位2人の割合（偶然なら約 2/7）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S196共', '../S196_一緒にいる相手を選ぶ_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 組(o, lo, hi):
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; n = A.shape[1]; R = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(n):
            if i != j: m = 相[:, i] == j + 1; R[i, j] = (A[m, i] == 3).mean() if m.any() else np.nan
    x, y = [], []
    for i in range(n):
        for j in range(i + 1, n): x.append(R[i, j]); y.append(R[j, i])
    x, y = np.array(x), np.array(y); ok = ~np.isnan(x) & ~np.isnan(y)   # S196：会わなかった組は除く
    相関 = float(np.corrcoef(x[ok], y[ok])[0, 1]) if ok.sum() >= 3 else float('nan')
    偏り = float(np.mean([np.sort(np.nan_to_num(R[i][~np.isnan(R[i])]))[-2:].sum() / max(np.nansum(R[i]), 1e-9) for i in range(n)]))
    return 相関, 偏り
def 会う偏り(o, lo, hi):
    相 = o['相手列'][lo:hi]; n = 相.shape[1]; r = []
    for i in range(n):
        c = np.bincount(相[:, i][(相[:, i] > 0) & (相[:, i] <= n)], minlength=n + 1)[1:]; c = np.delete(c, i); r.append(np.sort(c)[-2:].sum() / max(c.sum(), 1))
    return float(np.mean(r))
def 測る(s, β, kG=1.0, 寿命=8000):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=β)
    if 寿命 < 8000: return o['sha256']
    return 組(o, 6000, 8000) + (会う偏り(o, 6000, 8000), o['sha256'])
