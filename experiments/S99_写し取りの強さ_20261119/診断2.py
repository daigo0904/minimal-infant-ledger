"""調整用の種 900〜909：kM=2・代替わりの作りで、500手ごとに「入れ替わった子（自由な子）」の仲間前しきたり率と、自由な子の数。"""
import numpy as np
from multiprocessing import Pool
from 共通 import *
代 = dict(しきたり始め=2000, 代替わり=4000, 代替わり間隔=500)
def one(job):
    s, kM = job; o = 一生(s, '決まった手', True, kM, 寿命=10000, **代); A = o['行動列']; 相 = o['相手列']; x = しきたりの手(s); 当 = o['当たり'][0]
    out = []
    for b in range(4000, 10000, 500):
        自由 = [j for j in range(8) if b >= 4000 + j * 500]
        m = np.concatenate([(A[b:b + 500, j][相[b:b + 500, j] > 0] == x) for j in 自由]); n = np.concatenate([(A[b:b + 500, j] == 当) for j in 自由])
        out.append((float(m.mean()), float(n.mean())))
    return out
if __name__ == '__main__':
    with Pool(8) as p:
        for kM in [0.0, 2.0]:
            r = np.array(p.map(one, [(s, kM) for s in range(900, 910)]))
            print(f'kM={kM}  区の始め: 自由な子の数 / 仲間前しきたり / 当たり')
            for i, b in enumerate(range(4000, 10000, 500)): print(f'  {b}: {min(8, (b - 4000) // 500 + 1)}人  {np.median(r[:, i, 0]):.3f}  {np.median(r[:, i, 1]):.3f}')
