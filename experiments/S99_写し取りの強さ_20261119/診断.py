"""調整用の種 900〜909：S95 の新入りのしきたり率を、見ている相手（仲間／養育者）で分ける。時期でも分ける。"""
import numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S95R', '../S95_意味のないしきたり_20261119/走らせる.py')
def one(job):
    s, 型 = job; o = R.一生(s, 型, True); A = o['行動列'][:, 7]; 相 = o['相手列'][:, 7]; x = R.しきたりの手(s)
    f = lambda lo, hi, m: float((A[lo:hi][m(相[lo:hi])] == x).mean())
    return [f(4000, 4500, lambda w: w > 0), f(4500, 6000, lambda w: w > 0), f(4500, 6000, lambda w: w == 0), f(5500, 6000, lambda w: w > 0)]
if __name__ == '__main__':
    with Pool(8) as p:
        for 型 in ['でたらめ', '決まった手']:
            r = np.array(p.map(one, [(s, 型) for s in range(900, 910)]))
            print(型, '仲間が見る 4000-4500 %.3f | 4500-6000 仲間 %.3f 養育者 %.3f | 5500-6000 仲間 %.3f' % tuple(np.median(r, 0)))
