"""調整用の種 900〜909：視線を直に足す頭（直）と元の頭（混ぜる）で、S109（切替なし）と S110（4000 で仲間へ）を見る。"""
import numpy as np
from multiprocessing import Pool
from 共通2 import *
def one(job):
    s, 腕, 直, 切 = job; o = 一生(s, 4, 腕, 学び率=0.01, 視線切替=切, 視線直=直)
    return 追う(o, 0, 500) + 追う(o, 3500, 4000) + 追う(o, 4000, 5000) + 追う(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 直 in [False, True]:
            for 切 in [None, 4000]:
                for 腕 in ['本物', 'ずらし']:
                    m = np.median(np.array(p.map(one, [(s, 腕, 直, 切) for s in range(900, 910)])), 0)
                    print(f'直={直} 切替={切} {腕}: 0-500 養{m[0]:.3f} 他{m[1]:.3f} | 3500-4000 養{m[2]:.3f} 他{m[3]:.3f} | 4000-5000 養{m[4]:.3f} 他{m[5]:.3f} | 7000-8000 養{m[6]:.3f} 他{m[7]:.3f}')
