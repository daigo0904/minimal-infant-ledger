import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S193_感謝とお返し_20261121'); import 数え; return 数え.測る(900, x, 寿命=1500)
def 旧(_):
    sys.path.insert(0, '../S190_なぐさめの代価_20261121'); import 共; return 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03)['sha256']
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a, b, c = p.map(新, [None, 0.0, 3.0], chunksize=1); d = p.map(旧, [0])[0]
    print('感謝なし＝S190:', a == d, ' 入力だけ(kG0)で変わる:', a != b, ' kG3 で変わる:', b != c)
