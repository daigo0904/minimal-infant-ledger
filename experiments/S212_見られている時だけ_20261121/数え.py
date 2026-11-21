"""S212：S211 の数え方（β0・寿命16000・選び替え 2000手から250手ごと・はじめ 子0〜3 親切・kG1）に、観客ありの手と なしの手の なぐさめの割合（仲間の番・後半8000手・子の平均）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S212共', '../S212_見られている時だけ_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, kG=1.0, β=0.0, 選=(2000, 250), 寿命=16000, 親切=3.0, δ=0.0, ρ=0.0, 観=False, 見評=False):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=β, 困寄る=0.0, 親切=親切, 親切組=(0, 1, 2, 3), 選び替え=選, 同類=δ, 評判=ρ, 観客入力=観, 見られ評判=見評)
    if 寿命 < 16000: return o['sha256']
    x = o['親切数列']; h = 寿命 // 2; A, 相, 観 = o['行動列'][h:], o['相手列'][h:], o['観客列'][h:]; 仲 = (相 > 0) & (相 <= 8)
    あり = float(((A == 3) & 仲 & 観).sum() / max(1, (仲 & 観).sum())); なし = float(((A == 3) & 仲 & ~観).sum() / max(1, (仲 & ~観).sum()))
    d = []   # 同じ子（同じ席・250手の区切り＝選び替えの間は同じ子）の中で、観客あり−なし。子の違い（評判の高い子ほど見られ、よくなぐさめる）を消す
    for b in range(0, h, 250):
        for i in range(8):
            a, m, v = A[b:b + 250, i] == 3, 仲[b:b + 250, i], 観[b:b + 250, i]
            if (m & v).sum() >= 5 and (m & ~v).sum() >= 5: d.append(a[m & v].mean() - a[m & ~v].mean())
    return float(np.mean(x[-8:])), float(np.mean(d)), あり - なし, あり, なし, float((仲 & 観).sum() / max(1, 仲.sum())), o['sha256']
