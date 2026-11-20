import sys, numpy as np
sys.path.insert(0, '../S203_親切な転入生_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:7]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in [1.0, 3.0]}
    for k, r in R.items(): m = np.median(r, 0); print(f'親切{k}: なぐさめてもらった差 ' + ' '.join(f'{v:+.0f}' for v in m[:3]) + ' 入り次数の差 ' + ' '.join(f'{v:+.2f}' for v in m[3:6]) + f' 転入生の手3 {m[6]:.3f}')
    a, b = R[3.0], R[1.0]; print('親切>ふつう（0〜1000）：入り次数', int((a[:,3] > b[:,3]).sum()), '/10 なぐさめてもらった', int((a[:,0] > b[:,0]).sum()), '/10 手3', int((a[:,6] > b[:,6]).sum()), '/10')
