"""S228：後半の 当たり率、全体の 合図と場所の相互情報量、話し手ごとの相互情報量の平均（その子の言い方のはっきりさ）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S228共', '../S228_二人だけの言葉_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 相互(x, y):
    J = np.zeros((4, 4)); np.add.at(J, (x, y), 1); J /= J.sum(); px, py = J.sum(1, keepdims=True), J.sum(0, keepdims=True); m = J > 0
    return float((J[m] * np.log2(J[m] / (px @ py)[m])).sum())
def 測る(s, 組み方='毎回', kE=50.0, 見える=False, 寿命=16000):
    o = C.一生(s, 寿命, kE, 見える, 組み方); h = 寿命 // 2
    合, 場, 当, 話 = o['合列'][h:].ravel(), o['場列'][h:].ravel(), o['当列'][h:].ravel(), o['話列'][h:].ravel()
    個 = [相互(場[話 == i], 合[話 == i]) for i in range(8) if (話 == i).sum() > 100]
    return float(当.mean()), 相互(場, 合), float(np.mean(個)), o['sha256']
