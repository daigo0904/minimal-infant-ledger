import sys, numpy as np
sys.path.insert(0, '../S188_なぐさめ_20261121')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, 名, k = job; o = 一生(s, 名, なぐさめ=True, kE=k); A, 相 = o['行動列'][7000:], o['相手列'][7000:]
    return なぐさめ方(o, 7000, 8000) + (float((A[相 > 0] == 3).mean()), float(o['食列'][7000:].mean()), 共.__dict__.get('x', 0) if False else 0.0)
import 共
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名, k in [('元', 0.0), ('v4', 0.0), ('v4', 5.0), ('v4', 20.0), ('v4', 50.0)]:
            r = np.array(p.map(one, [(s, 名, k) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{名} kE{k}: なぐさめ 困っている−いない {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 困っている時 {m[1]:.3f} いない時 {m[2]:.3f} 仲間の前の手3 {m[4]:.3f} 相手の空腹 {m[3]:.3f} 食べ {m[5]:.4f}', flush=True)
