import sys, numpy as np
sys.path.insert(0, '../S137_覚えた順番交代は保たれるか_20261119')
from multiprocessing import Pool
from 共 import *
腕 = [('交代', None), ('交代', '褒めだけ'), ('交代', 'でたらめ')]
def one(job): s, 番, 後 = job; o = 一生(s, 番, 番後=後); return 数える(o, 3000, 4000) + 数える(o, 4000, 5000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 番, 後 in 腕:
            r = np.array(p.map(one, [(s, 番, 後) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'後={後}: 差 3000〜4000 {m[2]:+.3f} | 4000〜5000 {m[6]:+.3f} | 7000〜8000 {m[10]:+.3f}  話す時に声 {m[1]:.3f}→{m[9]:.3f} 食べ {m[11]:.4f}')
