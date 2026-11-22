"""S237：耳で話す・16か所（未見なし）。(1) 選び替え：はじめ 分けて聞く子 0〜3、終わり＝最後の8回の分けて聞く子の数。(2) 型固定：分けて4・まとめて4、席を入れ替えた2一生、後半8000手の空腹 まとめて−分けて（正＝分けて聞く子が得）と、聞き手としての当たり率 分けて／まとめて。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S237共', '../S237_聞き方は受け継がれるか_20261122/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 増える(s, 寿命=16000):
    o = C.一生(s, 寿命, 50.0, '耳', None, '型', (0, 1, 2, 3), (2000, 250)); x = o['分数列']; return float(np.mean(x[-8:])), o['sha256']
def 得(s, 寿命=16000):
    r, a, b = [], [], []
    for 分 in [(0, 1, 2, 3), (4, 5, 6, 7)]:
        o = C.一生(s, 寿命, 50.0, '耳', None, '型', 分, None); H = o['h列'][len(o['h列']) // 2:]; ま = [i for i in range(8) if i not in 分]
        r.append(H[:, ま].mean() - H[:, list(分)].mean()); h = 寿命 // 2; 聞, 当 = o['聞'][h:].ravel(), o['当列'][h:].ravel()
        a.append(当[np.isin(聞, 分)].mean()); b.append(当[~np.isin(聞, 分)].mean())
    return float(np.mean(r)), float(np.mean(a)), float(np.mean(b)), o['sha256']
