"""調整用の種 900〜909：S110 の作り（切替 4000）で、仲間が見ている時の手が「仲間の直前の手」「仲間の視線」に合う割合。仲間が褒める／褒めない。"""
import numpy as np
from multiprocessing import Pool
from 共通2 import *
import 共通2
def one(job):
    s, 腕, 褒 = job
    原 = N.一生
    def 包(*a, **k): k['仲間は褒めない'] = not 褒; return 原(*a, **k)
    N.一生 = 包
    try: o = 一生(s, 4, 腕, 学び率=0.01, 視線切替=4000)
    finally: N.一生 = 原
    A, 相, 視 = o['行動列'], o['相手列'], o['視線列']
    前 = np.vstack([A[:1] * 0 - 1, A[:-1]])   # 直前の手（t=0 は無し）
    out = []
    for lo, hi in [(3000, 4000), (4000, 5000), (7000, 8000)]:
        a, w = A[lo:hi], 相[lo:hi]; m = w > 0
        仲前 = np.take_along_axis(前[lo:hi], np.maximum(w - 1, 0), axis=1); 仲視 = np.take_along_axis(視[lo:hi], w, axis=1)
        out += [float((a[m] == 仲前[m]).mean()), float((a[m] == 仲視[m]).mean())]
    return out
if __name__ == '__main__':
    with Pool(8) as p:
        for 褒 in [True, False]:
            for 腕 in ['本物', 'ずらし']:
                m = np.median(np.array(p.map(one, [(s, 腕, 褒) for s in range(900, 910)])), 0)
                print(f'仲間が褒める={褒} 前半{腕}: 3000-4000 直前の手{m[0]:.3f} 視線{m[1]:.3f} | 4000-5000 直前{m[2]:.3f} 視線{m[3]:.3f} | 7000-8000 直前{m[4]:.3f} 視線{m[5]:.3f}')
