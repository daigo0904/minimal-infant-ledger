"""S226：S225 の数え方（v4＋共感・泣き・代価・感謝kG1・β0・評判なし・型なし・選び替えなし・寿命16000・公平入力あり）に 公平の報酬 kQ。
後半8000手：少ない−多い（S225 と同じ）、受けたなぐさめの回数の 8人の変動係数（標準偏差/平均）、空腹の8人のばらつき（標準偏差）、なぐさめの割合。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S226共', '../S226_公平の気持ち_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, kQ=0.0, 公平=True, 寿命=16000):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=1.0, 親切組=(), 選び替え=None, 公平入力=公平, kQ=kQ)
def 測る(s, kQ=0.0, 寿命=16000):
    o = 一生(s, kQ, True, 寿命); h = 寿命 // 2; A, U, 相 = o['行動列'][h:], o['相受列'][h:], o['相手列'][h:]; d = []
    for i in range(8):
        m = ~np.isnan(U[:, i]); a, u = A[m, i] == 3, U[m, i]; 中 = np.median(u)
        if (u < 中).sum() > 50 and (u > 中).sum() > 50: d.append(a[u < 中].mean() - a[u > 中].mean())
    受 = np.array([((A == 3) & (相 == k + 1)).sum() for k in range(8)], float)
    H = o['h列'][len(o['h列']) // 2:]
    return float(np.mean(d)), float(受.std() / 受.mean()), float(H.mean(0).std()), float((A == 3).mean()), o['sha256']
