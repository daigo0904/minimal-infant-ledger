import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S171_取りたくなる悪い物_20261120'); import 共
    return 共.一生(900, '見る', 'v4', 1500, 種類=(700,), k代理=3.0, 何でも=1, 似せる=x)['sha256']
def 旧(_):
    sys.path.insert(0, '../S170_失敗を見せる仲間_20261120'); import 共
    return 共.一生(900, '見る', 'v4', 1500, 種類=(700,), k代理=3.0, 何でも=1)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [None, 0.2], chunksize=1); c = p.map(旧, [0])[0]
    print('似せない＝S170:', a == c, a[:8], ' 似せると変わる:', a != b)
