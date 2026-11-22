import sys, numpy as np
sys.path.insert(0, '../S196_一緒にいる相手を選ぶ_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, β, k = job; return 数え.測る(s, β, kG=k)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {(β, k): np.array(p.map(one, [(s, β, k) for s in range(900, 910)], chunksize=1)) for β, k in [(0.3, 0.0), (0.3, 1.0)]}
    for key, r in R.items(): m = np.nanmedian(r, 0); print(f'β{key[0]} kG{key[1]}: 相関 {m[0]:+.3f} なぐさめ先の偏り {m[1]:.3f} 会う偏り {m[2]:.3f}')
    a, b = R[(0.3, 1.0)], R[(0.3, 0.0)]
    print('kG1 > kG0（β0.3）：なぐさめ先の偏り', int((a[:,1] > b[:,1]).sum()), '/10 会う偏り', int((a[:,2] > b[:,2]).sum()), '/10 相関', int((a[:,0] > b[:,0]).sum()), '/10')
