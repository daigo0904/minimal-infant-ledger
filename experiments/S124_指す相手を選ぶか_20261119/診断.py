import numpy as np
from multiprocessing import Pool
from 共 import *
def one(job): s, 効 = job; o = 一生(s, 効); return 数える(o, 0, 1000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 効 in [True, False]:
            m = np.median(np.array(p.map(one, [(s, 効) for s in range(900, 910)])), 0)
            print(f'効く={効}: 初め 指す 養{m[0]:.3f} 仲{m[1]:.3f} 当たりを指す 養{m[2]:.3f} 仲{m[3]:.3f} | 終わり 指す 養{m[4]:.3f} 仲{m[5]:.3f} 当たりを指す 養{m[6]:.3f} 仲{m[7]:.3f}')
