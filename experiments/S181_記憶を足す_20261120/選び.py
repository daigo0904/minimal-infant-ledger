import sys, numpy as np
sys.path.insert(0, '../S181_記憶を足す_20261120')
from multiprocessing import Pool
def one(job):
    import 数え; s, 名, α = job; return 数え.測る(s, 名, True, 'いない時', 記憶=α)[:11]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名, α in [('v4', None), ('v4', 0.3), ('v4', 0.5), ('v4', 0.8), ('元', 0.5)]:
            r = np.array(p.map(one, [(s, 名, α) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{名} 記憶{α}: 指す差 終わり {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） ／ 知らない時に指す {m[6]:.3f} 知っている時に指す {m[7]:.3f} 知っている時に取る {m[8]:.3f} 知らない時に取る {m[9]:.3f} 食べ {m[10]:.4f}', flush=True)
