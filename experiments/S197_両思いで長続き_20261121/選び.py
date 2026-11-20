import sys, numpy as np
sys.path.insert(0, '../S197_両思いで長続き_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, b, kk) for s in range(900, 910)], chunksize=1)) for k, (b, kk) in {'β0_kG1': (0.0, 1.0), 'β0.3_kG0': (0.3, 0.0), 'β0.3_kG1': (0.3, 1.0)}.items()}
    for k, r in R.items(): m = np.median(r, 0); print(f'{k}: 両思い {m[0]:.3f}（偶然 0.143） 長続き {m[1]:.3f}（偶然 0.143）')
    a, b, c = R['β0.3_kG1'], R['β0.3_kG0'], R['β0_kG1']
    print('kG1>kG0（β0.3）：両思い', int((a[:,0] > b[:,0]).sum()), '/10 長続き', int((a[:,1] > b[:,1]).sum()), '/10  β0.3kG1 両思い>0.143', int((a[:,0] > 0.143).sum()), '/10 長続き>0.143', int((a[:,1] > 0.143).sum()), '/10')
