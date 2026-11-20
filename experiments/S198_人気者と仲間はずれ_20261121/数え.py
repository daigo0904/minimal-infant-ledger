"""S198：S196 の世界・頭をそのまま読む（6000〜8000）。top(i)＝i を一番よく見た仲間。外れ＝誰の top でもない子（偶然の目安 8·(6/7)^7≈2.7人）。
外れた子と他の子の 空腹（h列の平均）・なぐさめてもらった回数 の差（外れ − 他、外れがいる世界だけ）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S196共', '../S196_一緒にいる相手を選ぶ_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, β, kG, lo=6000, hi=8000):
    o = C.一生(s, 'v4', なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=β)
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; n = A.shape[1]; M = np.zeros((n, n)); 受 = np.zeros(n)
    for i in range(n):
        c = np.bincount(相[:, i][(相[:, i] > 0) & (相[:, i] <= n)], minlength=n + 1)[1:]; c[i] = -1; M[i] = c
        m = (A[:, i] == 3) & (相[:, i] > 0) & (相[:, i] <= n)
        for k in 相[:, i][m]: 受[k - 1] += 1   # i がなぐさめた相手 k−1 は「なぐさめてもらった」
    top = M.argmax(1); 入 = np.bincount(top, minlength=n); 外 = 入 == 0
    h = o['h列'][lo // 100:hi // 100].mean(0)
    差h = float(h[外].mean() - h[~外].mean()) if 外.any() and (~外).any() else np.nan
    差受 = float(受[外].mean() - 受[~外].mean()) if 外.any() and (~外).any() else np.nan
    x = np.sort(入); ジニ = float((2 * np.arange(1, n + 1) - n - 1) @ x / (n * x.sum()))
    return int(外.sum()), ジニ, 差h, 差受, o['sha256']
