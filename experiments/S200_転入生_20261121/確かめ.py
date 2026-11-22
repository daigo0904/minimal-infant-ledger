import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S200_転入生_20261121'); import 数え; return 数え.測る(900, 5.0, 転入=x, 寿命=1500)
def 旧(_):
    sys.path.insert(0, '../S199_困っている子にも寄る_20261121'); import 数え; return 数え.測る(900, 5.0, 寿命=1500)
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [None, 700], chunksize=1); c = p.map(旧, [0])[0]
    print('転入なし＝S199（γ5）:', a == c, ' 転入で変わる:', a != b)
