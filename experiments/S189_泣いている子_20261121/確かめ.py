import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S189_泣いている子_20261121'); import 共; o = 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=x); return o['sha256'], 共.泣きなぐさめ(o, 500, 1500)[3:]
def 旧(_):
    sys.path.insert(0, '../S188_なぐさめ_20261121'); import 共; return 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ')['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: (a, x), (b, y) = p.map(新, [0.0, 0.02], chunksize=1); c = p.map(旧, [0])[0]
    print('泣きなし＝S188:', a == c, ' 泣きで変わる:', a != b)
    print('相手の空腹 泣きなし：>0.5 の割合・90%点・中央値', [round(v, 3) for v in x], ' 泣き0.02：', [round(v, 3) for v in y])
