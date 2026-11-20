import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S178_生まれつきの自分の好み_20261120'); import 共; return 共.一生(900, 'v4', 1500, 二人=0.5, 自分=0.05, k生まれ=x)['sha256']
def 旧(_):
    sys.path.insert(0, '../S176_本物のブロッコリー課題_20261120'); import 共; return 共.一生(900, 'v4', 1500, 二人=0.5, 自分=0.05)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [0.0, 0.3], chunksize=1); c = p.map(旧, [0])[0]
    print('生まれつき0＝S176:', a == c, ' 生まれつきで変わる:', a != b)
