import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S199_困っている子にも寄る_20261121'); import 数え; return 数え.測る(900, x, 寿命=1500)
def 旧(_):
    sys.path.insert(0, '../S196_一緒にいる相手を選ぶ_20261121'); import 共; return 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.3)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [0.0, 5.0], chunksize=1); c = p.map(旧, [0])[0]
    print('γ0＝S196（β0.3 kG1）:', a == c, ' γ5 で変わる:', a != b)
