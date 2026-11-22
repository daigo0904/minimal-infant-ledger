import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S190_なぐさめの代価_20261121'); import 共; return 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=x)['sha256']
def 旧(_):
    sys.path.insert(0, '../S189_泣いている子_20261121'); import 共; return 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [0.0, 0.03], chunksize=1); c = p.map(旧, [0])[0]
    print('代価0＝S189:', a == c, ' 代価で変わる:', a != b)
