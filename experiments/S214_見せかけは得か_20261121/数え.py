"""S214：S213 の世界・頭をそのまま読み（世界は変えない）、選び替えなし（型は一生固定）。後半8000手の型ごとの平均空腹（h列＝100手ごと）。
見せかけ−いつも親切 の空腹差（負＝見せかけが得）。席の違いを消すため、見せかけを子2,3 にした一生と 子0,1 にした一生の平均。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S214共', '../S213_見せかけの型_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, 見評, 見せ組, 寿命=16000):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=(0, 1, 2, 3), 選び替え=None, 同類=0.0, 評判=5.0, 観客入力=True, 見られ評判=見評, 見せ組=見せ組)
def 測る(s, 見評=True, 寿命=16000):
    r = []
    for 見, 常 in [((2, 3), (0, 1)), ((0, 1), (2, 3))]:
        o = 一生(s, 見評, 見, 寿命); H = o['h列'][len(o['h列']) // 2:]
        r.append((H[:, list(見)].mean() - H[:, list(常)].mean(), H[:, list(見)].mean(), H[:, list(常)].mean(), H[:, 4:].mean(), o['sha256']))
    return float(np.mean([x[0] for x in r])), float(np.mean([x[1] for x in r])), float(np.mean([x[2] for x in r])), float(np.mean([x[3] for x in r])), r[0][4]
