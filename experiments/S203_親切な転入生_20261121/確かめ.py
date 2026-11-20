import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S203_親切な転入生_20261121'); import 数え; return 数え.測る(900, x, 寿命=3000)
def 旧(_):
    sys.path.insert(0, '../S201_転入生を何度も_20261121'); import 共
    return 共.一生(900, 'v4', 3000, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.3, 困寄る=0.0, 転入=[(2000 + 1000 * k, k) for k in range(4)])['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [1.0, 3.0], chunksize=1); c = p.map(旧, [0])[0]
    print('親切1＝S202 の作り:', a == c, ' 親切3 で変わる:', a != b)
