import sys, numpy as np
sys.path.insert(0, '../S156_値打ちか選び方か_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 正直 = job; return 数える(一生(s, '養育者', 物知り=(1, 正直), 記録=True), s, (1, 正直))
if __name__ == '__main__':
    名 = ['正体ごとの取る差', '顔ごとの取る差', '余裕の差', '食べ予測の差', '癖の差']
    with Pool(8, maxtasksperchild=1) as p:
        r = {正直: np.array(p.map(one, [(s, 正直) for s in range(900, 910)], chunksize=1)) for 正直 in [1.0, 0.7]}
    for j, n in enumerate(名):
        a, b = np.median(r[1.0][:, j]), np.median(r[0.7][:, j]); 比 = r[0.7][:, j] / r[1.0][:, j]
        print(f'{n}: 1.0 {a:+.3f} 0.7 {b:+.3f} 比(中央値の比) {b/a:.3f} 世界ごとの比の中央値 {np.median(比):.3f}')
