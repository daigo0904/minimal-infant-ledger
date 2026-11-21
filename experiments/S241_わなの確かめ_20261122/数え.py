"""S241：4か所・毎回組み替え・ふつうに話す。8000手まで協力、8000から競う。当たり率 競い始め前（4000〜8000）／最後（12000〜16000）、全体の結びつき（同じ窓）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S241共', '../S241_わなの確かめ_20261122/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 相互(x, y):
    J = np.zeros((4, 4)); np.add.at(J, (x, y), 1); J /= J.sum(); px, py = J.sum(1, keepdims=True), J.sum(0, keepdims=True); m = J > 0
    return float((J[m] * np.log2(J[m] / (px @ py)[m])).sum())
def 測る(s, kE=50.0, 寿命=16000, 始め=8000):
    o = C.一生(s, 寿命, kE, False, '毎回', 'ふつう', None, None, None, True, 始め)
    def 窓(a, b): return float(o['当列'][a:b].mean()), 相互(o['場列'][a:b].ravel(), o['合列'][a:b].ravel())
    前 = 窓(始め - 4000, 始め); 後 = 窓(寿命 - 4000, 寿命); return 前[0], 後[0], 前[1], 後[1], o['sha256']
