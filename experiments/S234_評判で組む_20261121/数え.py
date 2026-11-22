"""S234：S233 の数え方に 組評判 ρ。(1) 選び替えの終わりの耳の子の数。(2) 型固定の空腹 ふつう−耳。参考：型固定で 耳どうしが組んだ割合（後半）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S234共', '../S234_評判で組む_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 増える(s, ρ=5.0, kE=50.0, 寿命=16000):
    o = C.一生(s, 寿命, kE, False, '毎回', '型', None, None, None, (0, 1, 2, 3), (2000, 250), ρ); x = o['耳数列']; return float(np.mean(x[-8:])), o['sha256']
def 得(s, ρ=5.0, kE=50.0, 寿命=16000):
    r, q = [], []
    for 耳 in [(0, 1, 2, 3), (4, 5, 6, 7)]:
        o = C.一生(s, 寿命, kE, False, '毎回', '型', None, None, None, 耳, None, ρ); H = o['h列'][len(o['h列']) // 2:]; 普 = [i for i in range(8) if i not in 耳]
        r.append(H[:, 普].mean() - H[:, list(耳)].mean()); h = 寿命 // 2; 話, 聞 = o['話列'][h:], o['聞列'][h:]; m = np.isin(話, 耳) & np.isin(聞, 耳); q.append(m.mean())
    return float(np.mean(r)), float(np.mean(q)), o['sha256']
