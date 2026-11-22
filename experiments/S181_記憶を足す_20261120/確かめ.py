import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S181_記憶を足す_20261120'); import 数え; return 数え.測る(900, 'v4', True, 'いない時', 寿命=1500, 記憶=x)
def 旧(_):
    sys.path.insert(0, '../S180_記憶が要る知らない_20261120'); import 数え; return 数え.測る(900, 'v4', True, 'いない時', 寿命=1500)
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [None, 0.5], chunksize=1); c = p.map(旧, [0])[0]
    print('記憶なし＝S180:', a == c, ' 記憶で変わる:', a != b)
