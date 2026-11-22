"""S199：S199 の世界（S196＋困寄る）。S198 の外れの数え方＋会う偏り（上位2人）＋両思い（S197）。6000〜8000。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S199共', '../S199_困っている子にも寄る_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, γ, β=0.3, kG=1.0, 寿命=8000, lo=6000, hi=8000):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=β, 困寄る=γ)
    if 寿命 < 8000: return o['sha256']
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; n = A.shape[1]; M = np.zeros((n, n)); 受 = np.zeros(n); 偏 = []
    for i in range(n):
        c = np.bincount(相[:, i][(相[:, i] > 0) & (相[:, i] <= n)], minlength=n + 1)[1:]; 偏.append(np.sort(np.delete(c, i))[-2:].sum() / max(np.delete(c, i).sum(), 1)); c[i] = -1; M[i] = c
        m = (A[:, i] == 3) & (相[:, i] > 0) & (相[:, i] <= n)
        for k in 相[:, i][m]: 受[k - 1] += 1
    top = M.argmax(1); 外 = np.bincount(top, minlength=n) == 0; h = o['h列'][lo // 100:hi // 100].mean(0)
    差h = float(h[外].mean() - h[~外].mean()) if 外.any() and (~外).any() else np.nan
    差受 = float(受[外].mean() - 受[~外].mean()) if 外.any() and (~外).any() else np.nan
    両 = float(np.mean([top[top[i]] == i for i in range(n)]))
    return 差h, 差受, float(np.mean(偏)), 両, float(h.mean()), int(外.sum()), o['sha256']
