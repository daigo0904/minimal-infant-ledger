"""S242：S238 の世界・頭をそのまま読み（世界は変えない）、頭の設定 kf（食べ予測の重み）だけ上書きする。競う・ふつうに話す・4か所・毎回組み替え。後半8000手の 当たり率、全体の結びつき、話し手ごとの結びつき。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S242共', '../S238_得がぶつかる世界_20261122/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 相互(x, y):
    J = np.zeros((4, 4)); np.add.at(J, (x, y), 1); J /= J.sum(); px, py = J.sum(1, keepdims=True), J.sum(0, keepdims=True); m = J > 0
    return float((J[m] * np.log2(J[m] / (px @ py)[m])).sum())
def 測る(s, kf=3.0, kE=50.0, 競う=True, 寿命=16000):
    元 = dict(C.構成['v4']); C.構成['v4']['kf'] = kf
    try: o = C.一生(s, 寿命, kE, False, '毎回', 'ふつう', None, None, None, 競う)
    finally: C.構成['v4'].clear(); C.構成['v4'].update(元)
    h = 寿命 // 2; 合, 場, 当, 話 = o['合列'][h:].ravel(), o['場列'][h:].ravel(), o['当列'][h:].ravel(), o['話列'][h:].ravel()
    return float(当.mean()), 相互(場, 合), float(np.mean([相互(場[話 == i], 合[話 == i]) for i in range(8)])), o['sha256']
