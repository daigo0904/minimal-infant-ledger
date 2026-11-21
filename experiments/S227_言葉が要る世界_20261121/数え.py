"""S227：後半の 当たり率、話し手の合図と場所の相互情報量（ビット・最大 2）、聞き手が合図に従う度合い（合図ごとの選んだ場所の相互情報量）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S227共', '../S227_言葉が要る世界_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 相互(x, y):
    J = np.zeros((4, 4))
    np.add.at(J, (x, y), 1); J /= J.sum(); px, py = J.sum(1, keepdims=True), J.sum(0, keepdims=True); m = J > 0
    return float((J[m] * np.log2(J[m] / (px @ py)[m])).sum())
def 測る(s, kE=50.0, 見える=False, 寿命=16000):
    o = C.一生(s, 寿命, kE, 見える); h = 寿命 // 2
    合, 場, 当 = o['合列'][h:].ravel(), o['場列'][h:].ravel(), o['当列'][h:].ravel()
    return float(当.mean()), 相互(場, 合), float(np.mean(o['h列'][len(o['h列']) // 2:])), o['sha256']
