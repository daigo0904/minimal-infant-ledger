import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S188_なぐさめ_20261121'); import 共; o = 共.一生(900, 'v4', 1500, なぐさめ=x[0], kE=x[1]); return o['sha256']
def 旧(_):
    sys.path.insert(0, '../S175_相手ごとの好み_20261120'); import 共; return 共.一生(900, 'v4', 1500)['sha256']
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a, b, c = p.map(新, [(False, 0.0), (True, 0.0), (True, 5.0)], chunksize=1); d = p.map(旧, [0])[0]
    print('口なし・共感なし＝S175:', a == d, ' 口で変わる:', a != b, ' 共感で変わる:', b != c)
