import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S174_親のそばは損が小さい_20261120'); import 共
    return 共.一生(900, '見る', 'v4', 1500, 守り=x)['sha256']
def 旧(_):
    sys.path.insert(0, '../S164_人見知り_20261120'); import 共
    return 共.一生(900, '見る', 'v4', 1500)['sha256']
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a, b, c = p.map(新, [None, 1.0, 0.2], chunksize=1); d = p.map(旧, [0])[0]
    print('守りなし＝S164(＝S173):', a == d, ' 守り1.0＝守りなし:', a == b, ' 守り0.2で変わる:', a != c)
