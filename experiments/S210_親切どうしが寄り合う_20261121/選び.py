import sys, numpy as np
sys.path.insert(0, '../S210_親切どうしが寄り合う_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k, δ = job; return 数え.測る(s, 1.0, β=0.3, 親切=k, δ=δ)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {(k, δ): np.array(p.map(one, [(s, k, δ) for s in range(900, 910)], chunksize=1)) for k, δ in [(3.0, 2.0), (1.0, 2.0)]}
    for key, r in R.items(): print(f'親切{key[0]} δ{key[1]}: 終わり {np.round(r[:,0], 1).tolist()}（中央値 {np.median(r[:,0]):.2f}）')
    a, c = R[(3.0, 2.0)], R[(1.0, 2.0)]; print('親切 > 対照:', int((a[:,0] > c[:,0]).sum()), '/10  親切 < 対照:', int((a[:,0] < c[:,0]).sum()), '/10  親切>4:', int((a[:,0] > 4).sum()), '/10')
