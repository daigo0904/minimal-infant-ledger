"""S200：転入生（子0）が 6000〜8000 で誰かの一番か（入り次数）・空腹・なぐさめてもらった回数を、ずっといる子（1〜7）の平均と比べる。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S200共', '../S200_転入生_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, γ, 転入=4000, 寿命=8000, lo=6000, hi=8000):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.3, 困寄る=γ, 転入=転入)
    if 寿命 < 8000: return o['sha256']
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; n = A.shape[1]; M = np.zeros((n, n)); 受 = np.zeros(n)
    for i in range(n):
        c = np.bincount(相[:, i][(相[:, i] > 0) & (相[:, i] <= n)], minlength=n + 1)[1:]; c[i] = -1; M[i] = c
        m = (A[:, i] == 3) & (相[:, i] > 0) & (相[:, i] <= n)
        for k in 相[:, i][m]: 受[k - 1] += 1
    入 = np.bincount(M.argmax(1), minlength=n); h = o['h列'][lo // 100:hi // 100].mean(0)
    return float(入[0]), float(入[1:].mean()), float(h[0] - h[1:].mean()), float(受[0] - 受[1:].mean()), o['sha256']
