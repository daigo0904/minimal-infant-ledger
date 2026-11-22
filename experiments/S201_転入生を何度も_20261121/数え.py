"""S201：3000手から1000手ごとに 子0〜4 を順に新しい子に。各転入生の来てから1000手の なぐさめてもらった回数・入り次数 を、同じ1000手の古株（2000手より前から いる子）の平均と比べ、5回の平均。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S201共', '../S201_転入生を何度も_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
予定 = [(3000 + 1000 * k, k) for k in range(5)]
def 測る(s, γ, 転入=True, 寿命=8000):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.3, 困寄る=γ, 転入=(予定 if 転入 else None))
    if 寿命 < 8000: return o['sha256']
    A, 相 = o['行動列'], o['相手列']; n = A.shape[1]; 受差, 入差 = [], []
    最後 = {k: -10**9 for k in range(n)}
    for tt, k in 予定:
        最後[k] = tt; lo, hi = tt, tt + 1000; a, w = A[lo:hi], 相[lo:hi]; 受 = np.zeros(n); M = np.zeros((n, n))
        for i in range(n):
            c = np.bincount(w[:, i][(w[:, i] > 0) & (w[:, i] <= n)], minlength=n + 1)[1:]; c[i] = -1; M[i] = c
            m = (a[:, i] == 3) & (w[:, i] > 0) & (w[:, i] <= n)
            for kk in w[:, i][m]: 受[kk - 1] += 1
        入 = np.bincount(M.argmax(1), minlength=n); 古 = [i for i in range(n) if 最後[i] <= tt - 2000]
        受差.append(受[k] - 受[古].mean()); 入差.append(入[k] - 入[古].mean())
    return float(np.mean(受差)), float(np.mean(入差)), o['sha256']
