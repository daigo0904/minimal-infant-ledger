"""S244：S243 の世界・頭をそのまま読む（世界は変えない。S243 の世界は S232 の転入・群れ・入れ替えの口を持つ）。ふつうに話す（耳の決まりなし）・協力・kE50・kf3・共感の見込み kC。
(a) 転入：t=8000 に子0 が新入り。最後4000手で新入りの 場所→一番多い合図 が 他の7人と一致する割合。
(b) 群れ m0.02：後半8000手で 群れの中の一致・群れどうしの一致。
(c) 入れ替え（2000から500手ごと）：1000〜2000 と 最後4000手 の皆の言い方の一致、最後の当たり率。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S244共', '../S243_共感の見込み_20261122/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 型(合, 場): return np.array([np.bincount(合[場 == l], minlength=4).argmax() for l in range(4)])
def 一生(s, 寿命, kC, 転入=None, 群れ=None, 入れ替え=None): return C.一生(s, 寿命, 50.0, False, '毎回', 'ふつう', 転入, 群れ, 入れ替え, False, kC)
def 転入(s, kC=10.0, 寿命=16000, t=8000):
    o = 一生(s, 寿命, kC, 転入=t); w = slice(寿命 - 4000, 寿命); c, l, sp = o['合列'][w].ravel(), o['場列'][w].ravel(), o['話列'][w].ravel()
    return float(np.mean(型(c[sp == 0], l[sp == 0]) == 型(c[sp != 0], l[sp != 0]))), o['sha256']
def 群れ(s, kC=10.0, 寿命=16000, m=0.02):
    o = 一生(s, 寿命, kC, 群れ=m); h = 寿命 // 2; c, l, sp = o['合列'][h:].ravel(), o['場列'][h:].ravel(), o['話列'][h:].ravel()
    T = np.array([型(c[sp == i], l[sp == i]) for i in range(8)])
    中 = np.mean([(T[i] == T[j]).mean() for i in range(8) for j in range(i + 1, 8) if i // 4 == j // 4]); 間 = np.mean([(T[i] == T[j]).mean() for i in range(8) for j in range(i + 1, 8) if i // 4 != j // 4])
    return float(中), float(間), o['sha256']
def 継承(s, kC=10.0, 寿命=16000):
    o = 一生(s, 寿命, kC, 入れ替え=(2000, 500)); 合, 場 = o['合列'], o['場列']; w = slice(寿命 - 4000, 寿命)
    return float(np.mean(型(合[1000:2000].ravel(), 場[1000:2000].ravel()) == 型(合[w].ravel(), 場[w].ravel()))), float(o['当列'][w].mean()), o['sha256']
