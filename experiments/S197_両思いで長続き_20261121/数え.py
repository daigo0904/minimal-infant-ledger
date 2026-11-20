"""S197：S196 の世界・頭をそのまま読む。M[i,j]＝i が j に見られた回数。一番の相手 top(i)=argmax M[i,:]。
両思い＝top(top(i))==i の子の割合（偶然の目安 1/7）。長続き＝4000〜6000 と 6000〜8000 で top が同じ子の割合（偶然 1/7）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S196共', '../S196_一緒にいる相手を選ぶ_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一番(o, lo, hi):
    相 = o['相手列'][lo:hi]; n = 相.shape[1]; M = np.zeros((n, n))
    for i in range(n):
        c = np.bincount(相[:, i][(相[:, i] > 0) & (相[:, i] <= n)], minlength=n + 1)[1:]; c[i] = -1; M[i] = c
    return M.argmax(1)
def 測る(s, β, kG):
    o = C.一生(s, 'v4', なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=β)
    a, b = 一番(o, 4000, 6000), 一番(o, 6000, 8000)
    両 = float(np.mean([b[b[i]] == i for i in range(len(b))])); 続 = float(np.mean(a == b))
    return 両, 続, o['sha256']
