import sys, numpy as np
sys.path.insert(0, '../S207_寄らないと親切は損か_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:5]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {(k, g): np.array(p.map(one, [(s, k, g) for s in range(900, 910)], chunksize=1)) for g in [1.0, 0.0] for k in [1.0, 3.0]}
    for g in [1.0, 0.0]:
        a, b = R[(3.0, g)], R[(1.0, g)]; d = a - b; m = np.median(d, 0)
        print(f'kG{g}（親切3−親切1 の 子0〜3−子4〜7 の差）: なぐさめてもらった {m[0]:+.0f}（>0 {int((d[:,0]>0).sum())}） 空腹 {m[2]:+.3f}（>0 {int((d[:,2]>0).sum())}） 食べ {m[3]:+.4f}（<0 {int((d[:,3]<0).sum())}） なぐさめた {m[4]:+.3f}')
    dg = (R[(3.0, 0.0)] - R[(1.0, 0.0)]) - (R[(3.0, 1.0)] - R[(1.0, 1.0)])
    print('感謝なしのほうが損（空腹の差が大きい）:', int((dg[:,2] > 0).sum()), '/10  なぐさめてもらった差が小さい:', int((dg[:,0] < 0).sum()), '/10')
