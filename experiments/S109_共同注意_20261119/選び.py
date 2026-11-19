"""調整用の種 900〜909：視線を追うことが育つか（K=4/8・学び率0.05/0.01・本物／ずらし）。"""
import numpy as np
from multiprocessing import Pool
from 共通2 import *
def one(job):
    s, K, lr, 腕 = job; o = 一生(s, K, 腕, 学び率=lr)
    return 追う(o, 0, 500) + 追う(o, 7000, 8000) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    C = [(K, lr) for K in [4, 8] for lr in [0.05, 0.01]]
    with Pool(8) as p:
        for K, lr in C:
            for 腕 in ['本物', 'ずらし']:
                r = np.array(p.map(one, [(s, K, lr, 腕) for s in range(900, 910)]))
                m = np.median(r, 0); print(f'K={K} lr={lr} {腕}: 初め 養{m[0]:.3f} 他{m[1]:.3f} | 終わり 養{m[2]:.3f} 他{m[3]:.3f} | 食べ {m[4]:.4f}  偶然 {1/K:.3f}')
