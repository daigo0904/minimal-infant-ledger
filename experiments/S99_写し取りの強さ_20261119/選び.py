"""調整用の種 900〜909 だけで、S95 の新入りがしきたりを写す割合を上げるつまみを探す。"""
import sys, json, numpy as np, importlib.util, itertools
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S95R', '../S95_意味のないしきたり_20261119/走らせる.py')
def one(job):
    s, c, ex, 型 = job
    R.B.c = c; R.W.探る = ex
    o = R.一生(s, 型, True); A = o['行動列']; x = R.しきたりの手(s)
    return (s, c, ex, 型, float((A[4500:6000, 7] == x).mean()), float(o['食列'][4500:6000, 7].mean()))
if __name__ == '__main__':
    J = [(s, c, ex, 型) for c in [30.0, 100.0, 300.0] for ex in [0.1, 0.03] for 型 in ['でたらめ', '決まった手'] for s in range(900, 910)]
    with Pool(8) as p: r = p.map(one, J)
    for c, ex in itertools.product([30.0, 100.0, 300.0], [0.1, 0.03]):
        g = lambda 型, k: float(np.median([v[k] for v in r if v[1] == c and v[2] == ex and v[3] == 型]))
        print(f'c={c:5} 探る={ex}: 決まった {g("決まった手",4):.3f} でたらめ {g("でたらめ",4):.3f}  食べ 決まった {g("決まった手",5):.3f}')
