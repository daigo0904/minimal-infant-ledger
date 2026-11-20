import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S195_恩を長く覚える_20261121'); import 数え; return 数え.測る(900, x, 寿命=1500)
def 旧(_):
    sys.path.insert(0, '../S193_感謝とお返し_20261121'); import 共; return 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [0.98, 0.998], chunksize=1); c = p.map(旧, [0])[0]
    print('0.98＝S193（kG1）:', a == c, ' 0.998 で変わる:', a != b)
