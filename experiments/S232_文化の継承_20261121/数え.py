"""S232：文化の継承。t=2000 から500手ごとに一番古い子を生まれたてに。皆の 場所→一番多い合図 を 1000〜2000手（最初の世代）と 最後の4000手 で比べた一致（4か所のうち）、最後の4000手の当たり率、最後の4000手の皆の言い方の一致（子どうし）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S232共', '../S232_文化の継承_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 型(合, 場): return np.array([np.bincount(合[場 == l], minlength=4).argmax() for l in range(4)])
def 測る(s, 話し方='耳', 寿命=16000, 入れ替え=(2000, 500)):
    o = C.一生(s, 寿命, 50.0, False, '毎回', 話し方, None, None, 入れ替え); 合, 場, 当, 話 = o['合列'], o['場列'], o['当列'], o['話列']
    前 = 型(合[1000:2000].ravel(), 場[1000:2000].ravel()); w = slice(寿命 - 4000, 寿命); 後 = 型(合[w].ravel(), 場[w].ravel())
    c, l, sp = 合[w].ravel(), 場[w].ravel(), 話[w].ravel(); 個 = np.array([型(c[sp == i], l[sp == i]) for i in range(8)])
    そろい = float(np.mean([(個[i] == 個[j]).mean() for i in range(8) for j in range(i + 1, 8)]))
    return float((前 == 後).mean()), float(当[w].mean()), そろい, o['sha256']
