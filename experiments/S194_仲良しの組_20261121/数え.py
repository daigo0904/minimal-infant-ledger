"""S194：S193 の世界・頭をそのまま読む。i が j に見られた手のうち i が手3 をした割合 R[i,j]（会う回数の差を消す）から、
(1) 組のそろい方＝R[i,j] と R[j,i] の相関（28組）、(2) なぐさめ先の偏り＝各子の R の上位2人の割合（偶然なら約 2/7）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S193共', '../S193_感謝とお返し_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 組(o, lo, hi):
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; n = A.shape[1]; R = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(n):
            if i != j: m = 相[:, i] == j + 1; R[i, j] = (A[m, i] == 3).mean() if m.any() else np.nan
    x, y = [], []
    for i in range(n):
        for j in range(i + 1, n): x.append(R[i, j]); y.append(R[j, i])
    相関 = float(np.corrcoef(x, y)[0, 1])
    偏り = float(np.mean([np.sort(np.nan_to_num(R[i][~np.isnan(R[i])]))[-2:].sum() / max(np.nansum(R[i]), 1e-9) for i in range(n)]))
    return 相関, 偏り
def 測る(s, kG):
    o = C.一生(s, 'v4', なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG); return 組(o, 6000, 8000) + (o['sha256'],)
