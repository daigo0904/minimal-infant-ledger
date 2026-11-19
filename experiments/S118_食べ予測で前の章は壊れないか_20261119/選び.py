import numpy as np
from multiprocessing import Pool
from 共 import *
def a(job): s, 腕, kf = job; return 見られ分け(s, 腕, kf)[1:]
def b(job): s, 型, kf = job; return しきたり(s, True, 型, kf)[1]
if __name__ == '__main__':
    with Pool(8) as p:
        for kf in [0.0, 3.0]:
            for 腕 in ['本物', 'ずらし']:
                m = np.median(np.array(p.map(a, [(s, 腕, kf) for s in range(900, 910)])), 0); print(f'S48 kf={kf} {腕}: 見られ分け 初め {m[0]:.3f} 終わり {m[1]:.3f}')
        m = np.median(np.array(p.map(a, [(s, '道具', 0.0) for s in range(900, 910)])), 0); print(f'S48 道具: 初め {m[0]:.3f} 終わり {m[1]:.3f}')
        for kf in [0.0, 3.0]:
            for 型 in ['決まった手', 'でたらめ']:
                print(f'S100 損の世界 多数 kf={kf} {型}: しきたり {np.median(p.map(b, [(s, 型, kf) for s in range(900, 910)])):.3f}')
