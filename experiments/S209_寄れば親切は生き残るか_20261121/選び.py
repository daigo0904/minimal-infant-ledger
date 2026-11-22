import sys, numpy as np, importlib.util
from multiprocessing import Pool
def one(job):
    sp = importlib.util.spec_from_file_location('S208数え', '../S208_損な親切は減るか_20261121/数え.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    s, β, k = job; return m.測る(s, 1.0, β=β, 親切=k)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {(β, k): np.array(p.map(one, [(s, β, k) for s in range(900, 910)], chunksize=1)) for β, k in [(0.3, 3.0), (0.3, 1.0)]}
    for key, r in R.items(): print(f'β{key[0]} 親切{key[1]}: 終わり {np.round(r[:,0], 1).tolist()} 中ほど {np.round(r[:,1], 1).tolist()}')
    a, c = R[(0.3, 3.0)], R[(0.3, 1.0)]; print('親切>0 の世界:', int((a[:,0] > 0).sum()), '/10  親切>4:', int((a[:,0] > 4).sum()), '/10  親切 > 対照:', int((a[:,0] > c[:,0]).sum()), '/10  親切 < 対照:', int((a[:,0] < c[:,0]).sum()), '/10')
