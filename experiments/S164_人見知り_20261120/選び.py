import sys, numpy as np
sys.path.insert(0, '../S164_人見知り_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 名 = job; o = 一生(s, '見る', 名, 知らない=(4000, 0.3)); return 人見(o, 4000, 4500) + 人見(o, 4000, 5000) + 人見(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名 in ['元', 'v4']:
            r = np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1))
            for k, w in enumerate(['4000-4500', '4000-5000', '7000-8000']):
                x = r[:, 8 * k:8 * k + 8]; 取差 = (x[:, 0] + x[:, 2]) / 2 - (x[:, 4] + x[:, 6]) / 2; 見差 = (x[:, 1] + x[:, 3]) / 2 - (x[:, 5] + x[:, 7]) / 2
                print(f'{名} {w}: 取る 知らない−仲間 {np.median(取差):+.3f}（<0 {int((取差 < 0).sum())}/10） 顔を見る 知らない−仲間 {np.median(見差):+.3f}（>0 {int((見差 > 0).sum())}/10） ／ 知らない 取る {np.median((x[:,0]+x[:,2])/2):.3f} 見る {np.median((x[:,1]+x[:,3])/2):.3f}', flush=True)
