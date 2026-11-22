"""S233：(1) 選び替え：はじめ 耳の子 0〜3、2000手から250手ごと、終わり＝最後の8回（2000手）の耳の子の数の平均。(2) 型固定（選び替えなし）：耳の子4・ふつう4、席を入れ替えた2一生、後半8000手の空腹 ふつう−耳（正＝耳が得）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S233共', '../S233_耳の型は増えるか_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 増える(s, kE=50.0, 寿命=16000):
    o = C.一生(s, 寿命, kE, False, '毎回', '型', None, None, None, (0, 1, 2, 3), (2000, 250)); x = o['耳数列']; return float(np.mean(x[-8:])), o['sha256']
def 得(s, kE=50.0, 寿命=16000):
    r = []
    for 耳 in [(0, 1, 2, 3), (4, 5, 6, 7)]:
        o = C.一生(s, 寿命, kE, False, '毎回', '型', None, None, None, 耳, None); H = o['h列'][len(o['h列']) // 2:]; 普 = [i for i in range(8) if i not in 耳]
        r.append(H[:, 普].mean() - H[:, list(耳)].mean())
    return float(np.mean(r)), o['sha256']
