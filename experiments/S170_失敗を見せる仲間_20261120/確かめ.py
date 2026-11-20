import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S170_失敗を見せる仲間_20261120'); import 共, numpy as np
    o = 共.一生(900, '見る', 'v4', 1500, 種類=(700,), k代理=3.0, 何でも=x); return o['sha256'], float((o['行動列'][:, 1] == 0).mean())
def 旧(_):
    sys.path.insert(0, '../S168_見て学ぶ_20261120'); import 共
    return 共.一生(900, '見る', 'v4', 1500, 種類=(700,), k代理=3.0)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: (a, _), (b, r1) = p.map(新, [None, 1], chunksize=1); c = p.map(旧, [0])[0]
    print('何でもなし＝S168:', a == c, a[:8], ' 何でもで手が変わる:', a != b, ' 赤ちゃん1が取る割合:', r1)
