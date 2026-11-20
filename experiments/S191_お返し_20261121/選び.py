import sys, numpy as np
sys.path.insert(0, '../S191_お返し_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for k in [0.0, 50.0]:
            r = np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'kE{k}: お返し（恩あり−なし）{m[0]:+.4f}（>0 {int((r[:,0]>0).sum())}/10） 恩あり {m[1]:.3f} 恩なし {m[2]:.3f} 恩ありの手数 {m[3]:.0f}', flush=True)
