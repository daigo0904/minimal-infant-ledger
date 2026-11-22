import sys, importlib.util
from multiprocessing import Pool
sys.path.insert(0, '../S138_一番の赤ちゃんv2_20261119')
_sp = importlib.util.spec_from_file_location('S138一覧', '../S138_一番の赤ちゃんv2_20261119/一覧.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def 元(w):
    _, M, Bm, _ = G.用意(w)   # 包まない（Bm.換算 は元のまま）
    if w == '122': M.A2.設定['kf'] = 0.0
    f = {'48': lambda: M.一生(900, '本物', 1500), '64': lambda: M.一生(900, '欠乏', 1500), '116': lambda: M.C.一生(900, 4, '本物', 寿命=1500, 学び率=0.01), '122': lambda: M.H.一生(900, 0.0, True, 寿命=1500), '125': lambda: M.一生(900, '褒める', 寿命=1500)}[w]
    return f()['sha256']
def 並び0(w): return G.並び((w, {}))
if __name__ == '__main__':
    with Pool(5, maxtasksperchild=1) as p: a = p.map(元, G.世界一覧); b = p.map(並び0, G.世界一覧)
    print('v2（全部0）は元と同じ:', dict(zip(G.世界一覧, [x == y for x, y in zip(a, b)])))
