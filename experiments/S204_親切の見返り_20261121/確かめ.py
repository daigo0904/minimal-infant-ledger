import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S204_親切の見返り_20261121'); import 数え; return 数え.測る(900, x, 寿命=1500)
def 旧(_):
    sys.path.insert(0, '../S199_困っている子にも寄る_20261121'); import 数え; return 数え.測る(900, 0.0, 寿命=1500)
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [1.0, 3.0], chunksize=1); c = p.map(旧, [0])[0]
    print('全員1倍＝S199（γ0）:', a == c, ' 親切3 で変わる:', a != b)
