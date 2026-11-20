"""S205：はじめ 子0〜3 親切（共感3倍）。2000手から500手ごとに 直近500手で一番お腹を空かせた子を新しい子にし、型は一番お腹の空いていない子から。親切な子の数の移り変わり。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S205共', '../S205_親切は広がるか_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, kG=1.0, 選=(2000, 500), 寿命=8000):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=0.3, 困寄る=0.0, 親切=3.0, 親切組=(0, 1, 2, 3), 選び替え=選)
    if 寿命 < 8000: return o['sha256']
    x = o['親切数列']; return float(np.mean(x[-2:])), float(x[3]) if len(x) > 3 else float('nan'), o['sha256']   # 終わりの親切数（最後の2回の平均）、2000手ごろ
