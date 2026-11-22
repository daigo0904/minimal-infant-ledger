"""S230：t=8000 に子0 が生まれたての新入りに。新入りの (a) 聞き手としての当たり率 来てすぐ 1000手／最後の4000手、(b) 最後の4000手の 話し手としての 場所→一番多い合図 が、他の7人の 場所→一番多い合図（7人まとめて）と一致する割合、参考に 他の7人どうしの一致。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S230共', '../S230_言葉の習得_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, 話し方='耳', 寿命=16000, 転入=8000):
    o = C.一生(s, 寿命, 50.0, False, '毎回', 話し方, 転入); 合, 場, 当, 話, 聞 = o['合列'], o['場列'], o['当列'], o['話列'], o['聞列']
    a1 = 当[転入:転入 + 1000][聞[転入:転入 + 1000] == 0].mean(); a2 = 当[寿命 - 4000:][聞[寿命 - 4000:] == 0].mean()
    w = slice(寿命 - 4000, 寿命); c, l, sp = 合[w].ravel(), 場[w].ravel(), 話[w].ravel()
    仲 = [np.bincount(c[(sp != 0) & (l == x)], minlength=4).argmax() for x in range(4)]
    新 = [np.bincount(c[(sp == 0) & (l == x)], minlength=4).argmax() for x in range(4)]
    return float(a1), float(a2), float(np.mean(np.array(新) == np.array(仲))), o['sha256']
