import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S211_評判で寄る_20261121'); import 数え; β, ρ = x; return 数え.測る(900, 1.0, β=β, 寿命=3000, 選=(1000, 250), ρ=ρ)
def 旧(x):
    sys.path.insert(0, '../S210_親切どうしが寄り合う_20261121'); import 数え; return 数え.測る(900, 1.0, β=x, 寿命=3000, 選=(1000, 250))
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a = p.map(新, [(0.3, 0.0), (0.0, 0.0), (0.0, 5.0)], chunksize=1); b = p.map(旧, [0.3, 0.0], chunksize=1)
    print('ρ0 β0.3＝S210:', a[0] == b[0], ' ρ0 β0＝S210:', a[1] == b[1], ' ρ5 β0 で変わる:', a[2] != a[1])
