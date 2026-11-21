"""S235：未見まで＝寿命−4000。組み立て度＝未見を出す前の最後の4000手（見る12か所）で、MI(合図1;行)+MI(合図2;列) と その入れ替え の大きいほう（最大 4 ビット）。全体の情報＝MI((合図1,合図2);場所)（最大 4）。当たり率（同じ窓）。未見の当たり＝最後の4000手のうち 最初の1000手／全部 の対角4か所の当たり率（偶然 1/16）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S235共', '../S235_組み合わせる言葉_20261122/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 相互(x, y, nx, ny):
    J = np.zeros((nx, ny)); np.add.at(J, (x, y), 1); J /= J.sum(); px, py = J.sum(1, keepdims=True), J.sum(0, keepdims=True); m = J > 0
    return float((J[m] * np.log2(J[m] / (px @ py)[m])).sum())
def 測る(s, 話し方='耳', 寿命=16000, kE=50.0):
    T = 寿命 - 4000; o = C.一生(s, 寿命, kE, 話し方, T); w = slice(max(0, T - 4000), T)
    a1, a2, r, c, 当 = (o[k][w].ravel() for k in ['a1', 'a2', '行', '列']), None, None, None, None
    a1, a2, r, c = (o[k][w].ravel() for k in ['a1', 'a2', '行', '列']); 当 = o['当列'][w].ravel()
    組 = max(相互(a1, r, 4, 4) + 相互(a2, c, 4, 4), 相互(a1, c, 4, 4) + 相互(a2, r, 4, 4)); 全 = 相互(a1 * 4 + a2, r * 4 + c, 16, 16)
    def 未見(lo, hi):
        R, Cc, A = o['行'][lo:hi].ravel(), o['列'][lo:hi].ravel(), o['当列'][lo:hi].ravel(); m = R == Cc; return float(A[m].mean())
    return 組, 全, float(当.mean()), 未見(T, T + 1000), 未見(T, 寿命), o['sha256']
