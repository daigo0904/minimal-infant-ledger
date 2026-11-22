"""調整用の種 900〜909：前半 本物／ずらし → 4000 から仲間の視線が意味を持つ。仲間の視線を追う割合の立ち上がり。"""
import numpy as np
from multiprocessing import Pool
from 共通2 import *
def one(job):
    s, 腕 = job; o = 一生(s, 4, 腕, 学び率=0.01, 視線切替=4000)
    return 追う(o, 3500, 4000) + 追う(o, 4000, 4500) + 追う(o, 4000, 5000) + 追う(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 腕 in ['本物', 'ずらし']:
            r = np.array(p.map(one, [(s, 腕) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'前半{腕}: 切替前 養{m[0]:.3f} 他{m[1]:.3f} | 4000-4500 他{m[3]:.3f} | 4000-5000 他{m[5]:.3f} | 7000-8000 他{m[7]:.3f} 養{m[6]:.3f}')
            print('   世界ごと 4000-4500 他:', np.round(r[:, 3], 3))
