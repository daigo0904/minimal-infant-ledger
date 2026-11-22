import sys, numpy as np
sys.path.insert(0, '../S179_知らない人に教える_20261120')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:10]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名 in ['元', 'v4']:
            r = np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{名}: 当たりを指す 知らない−知っている 終わり {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 初め {m[1]:+.3f} ／ 終わり 知らない時に指す {m[6]:.3f} 知っている時に指す {m[7]:.3f} 知っている時に取る {m[8]:.3f}', flush=True)
