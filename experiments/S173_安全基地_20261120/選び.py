import sys, numpy as np
sys.path.insert(0, '../S173_安全基地_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): return 測る(*job)[:12]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名 in ['元', 'v4']:
            r = np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{名}: 分からない物 取る 養育者−仲間 {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10）見る {m[1]:+.3f} ／ 手がかりあり 取る {m[2]:+.3f}（>0 {int((r[:,2]>0).sum())}/10）見る {m[3]:+.3f} ／ 分からない物 取る 養育者 {m[4]:.3f} 仲間 {m[6]:.3f}', flush=True)
            print(f'   分からない物の取る差 > 手がかりありの取る差: {int((r[:,0] > r[:,2]).sum())}/10')
