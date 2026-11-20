import sys, numpy as np
sys.path.insert(0, '../S193_感謝とお返し_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        R = {}
        for k in [None, 0.0, 1.0, 3.0]:
            r = np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)); R[k] = r; m = np.median(r, 0)
            print(f'kG{k}: お返し（恩あり−なし）{m[0]:+.4f}（>0 {int((r[:,0]>0).sum())}/10、>0.02 {int((r[:,0]>0.02).sum())}/10） 恩あり {m[1]:.3f} 恩なし {m[2]:.3f}', flush=True)
        for k in [1.0, 3.0]: print(f'kG{k} > kG0（入力だけ）: {int((R[k][:,0] > R[0.0][:,0]).sum())}/10')
