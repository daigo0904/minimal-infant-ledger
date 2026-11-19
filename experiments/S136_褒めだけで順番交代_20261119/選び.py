import sys, numpy as np
sys.path.insert(0, '../S136_褒めだけで順番交代_20261119')
from multiprocessing import Pool
from 頭 import *
def one(job): s, 番, λ = job; o = 一生λ(s, 番, λ); return 数える(o, 0, 1000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for λ in [1.0, 0.2]:
            for 番 in ['褒めだけ', '褒めだけでたらめ']:
                r = np.array(p.map(one, [(s, 番, λ) for s in range(900, 910)])); m = np.median(r, 0)
                print(f'λ={λ} {番}: 差 初め {m[2]:+.3f} → 終わり {m[6]:+.3f}（育つ {int((r[:,6] > r[:,2]).sum())}/10） 話す時に声 {m[1]:.3f}→{m[5]:.3f} 食べ {m[7]:.4f}')
