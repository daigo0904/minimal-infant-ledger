import sys, numpy as np
sys.path.insert(0, '../S198_人気者と仲間はずれ_20261121')
from multiprocessing import Pool
腕 = {'β0_kG1': (0.0, 1.0), 'β0.3_kG0': (0.3, 0.0), 'β0.3_kG1': (0.3, 1.0)}
def one(job):
    import 数え; s, 名 = job; return 数え.測る(s, *腕[名])[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1), dtype=float) for 名 in 腕}
    for 名, r in R.items(): m = np.nanmedian(r, 0); print(f'{名}: 外れの数 {m[0]:.1f}（偶然 2.7） ジニ {m[1]:.3f} 外れの空腹−他 {m[2]:+.3f}（>0 {int((r[:,2]>0).sum())}） なぐさめてもらった 外れ−他 {m[3]:+.1f}（<0 {int((r[:,3]<0).sum())}）')
