"""S204：子0〜3 が親切（共感量×親切）。6000〜8000 で 親切な子 − ふつうの子（子4〜7）の なぐさめてもらった回数・入り次数・空腹（h列）・食べ・なぐさめた割合。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S204共', '../S204_親切の見返り_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
親, 普 = [0, 1, 2, 3], [4, 5, 6, 7]
def 測る(s, 親切=3.0, kG=1.0, 寿命=8000, lo=6000, hi=8000):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=0.3, 困寄る=0.0, 親切=親切, 親切組=tuple(親))
    if 寿命 < 8000: return o['sha256']
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; n = A.shape[1]; M = np.zeros((n, n)); 受 = np.zeros(n)
    for i in range(n):
        c = np.bincount(相[:, i][(相[:, i] > 0) & (相[:, i] <= n)], minlength=n + 1)[1:]; c[i] = -1; M[i] = c
        m = (A[:, i] == 3) & (相[:, i] > 0) & (相[:, i] <= n)
        for k in 相[:, i][m]: 受[k - 1] += 1
    入 = np.bincount(M.argmax(1), minlength=n); h = o['h列'][lo // 100:hi // 100].mean(0); 食 = o['食列'][lo:hi].mean(0); 手 = (A == 3).mean(0)
    d = lambda x: float(x[親].mean() - x[普].mean())
    return d(受), d(入), d(h), d(食), d(手), o['sha256']
