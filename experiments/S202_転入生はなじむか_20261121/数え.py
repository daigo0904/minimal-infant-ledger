"""S202：S201 の世界・頭をそのまま読む。2000・3000・4000・5000手に 子0〜3 を順に新しい子に。各転入生の 来てから 0〜1000／1000〜2000／2000〜3000 手の
なぐさめてもらった回数 と 入り次数 を、同じ時間の古株（一度も入れ替えない 子4〜7）の平均と比べ（転入生−古株）、4人の平均。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S201共', '../S201_転入生を何度も_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
予定 = [(2000 + 1000 * k, k) for k in range(4)]; 古 = [4, 5, 6, 7]
def 窓(A, 相, lo, hi):
    n = A.shape[1]; a, w = A[lo:hi], 相[lo:hi]; 受 = np.zeros(n); M = np.zeros((n, n))
    for i in range(n):
        c = np.bincount(w[:, i][(w[:, i] > 0) & (w[:, i] <= n)], minlength=n + 1)[1:]; c[i] = -1; M[i] = c
        m = (a[:, i] == 3) & (w[:, i] > 0) & (w[:, i] <= n)
        for kk in w[:, i][m]: 受[kk - 1] += 1
    return 受, np.bincount(M.argmax(1), minlength=n)
def 測る(s, γ=0.0):
    o = C.一生(s, 'v4', 8000, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.3, 困寄る=γ, 転入=予定)
    A, 相 = o['行動列'], o['相手列']; 受差 = np.zeros((4, 3)); 入差 = np.zeros((4, 3))
    for j, (tt, k) in enumerate(予定):
        for w in range(3):
            受, 入 = 窓(A, 相, tt + 1000 * w, tt + 1000 * (w + 1)); 受差[j, w] = 受[k] - 受[古].mean(); 入差[j, w] = 入[k] - 入[古].mean()
    return tuple(受差.mean(0)) + tuple(入差.mean(0)) + (o['sha256'],)
