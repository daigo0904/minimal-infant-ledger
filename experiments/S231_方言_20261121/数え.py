"""S231：方言。後半8000手。子ごとの 場所→一番多い合図。群れの中の一致（同じ群れの2人の対・12組）、群れどうしの一致（またぐ対・16組）。当たり率 群れの中の組／またいだ組。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S231共', '../S231_方言_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, m=0.02, 話し方='耳', 寿命=16000):
    o = C.一生(s, 寿命, 50.0, False, '毎回', 話し方, None, m); h = 寿命 // 2
    合, 場, 当, 話, 聞 = o['合列'][h:].ravel(), o['場列'][h:].ravel(), o['当列'][h:].ravel(), o['話列'][h:].ravel(), o['聞列'][h:].ravel()
    型 = np.array([[np.bincount(合[(話 == i) & (場 == l)], minlength=4).argmax() for l in range(4)] for i in range(8)])
    群 = lambda i: i // 4
    中 = np.mean([(型[i] == 型[j]).mean() for i in range(8) for j in range(i + 1, 8) if 群(i) == 群(j)])
    間 = np.mean([(型[i] == 型[j]).mean() for i in range(8) for j in range(i + 1, 8) if 群(i) != 群(j)])
    同 = (話 // 4) == (聞 // 4)
    return float(中), float(間), float(当[同].mean()), float(当[~同].mean()) if (~同).sum() else float('nan'), o['sha256']
