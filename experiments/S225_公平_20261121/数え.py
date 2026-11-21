"""S225：公平。v4＋共感（kE50・苦しさ）・泣き0.01・代価0.03・感謝kG1・β0・評判なし・型なし（親切1）・選び替えなし・寿命16000。
後半8000手、仲間の番で、相手の受けた量が その子の中央値より 少ない時 − 多い時 の なぐさめ（手3）の割合（子ごと→平均）。参考に 相手の空腹 高い−低い の差。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S225共', '../S225_公平_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, 公平=False, 寿命=16000):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=1.0, 親切組=(), 選び替え=None, 公平入力=公平)
def 測る(s, 公平=False, 寿命=16000):
    o = 一生(s, 公平, 寿命); h = 寿命 // 2; A, U, H = o['行動列'][h:], o['相受列'][h:], o['相h列'][h:]; d, e = [], []
    for i in range(8):
        m = ~np.isnan(U[:, i]); a, u, x = A[m, i] == 3, U[m, i], H[m, i]; 中 = np.median(u)
        if (u < 中).sum() > 50 and (u > 中).sum() > 50: d.append(a[u < 中].mean() - a[u > 中].mean())
        中h = np.median(x); e.append(a[x > 中h].mean() - a[x <= 中h].mean())
    return float(np.mean(d)), float(np.mean(e)), float((A == 3).mean()), o['sha256']
