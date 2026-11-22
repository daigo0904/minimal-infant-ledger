import sys, numpy as np
sys.path.insert(0, '../S180_記憶が要る知らない_20261120')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:11]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名, 隠, 漂 in [('v4', False, 'いない時'), ('v4', True, 'いない時'), ('元', True, 'いない時'), ('v4', True, None)]:
            r = np.array(p.map(one, [(s, 名, 隠, 漂) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{名} 隠す{隠} 漂い{漂}: 指す差 知らない−知っている 終わり {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） ／ 知らない時に指す {m[6]:.3f} 知っている時に指す {m[7]:.3f} 知っている時に取る {m[8]:.3f} 知らない時に取る {m[9]:.3f} 食べ {m[10]:.4f}', flush=True)
