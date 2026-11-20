import sys
from multiprocessing import Pool
def f(x):
    sys.path.insert(0, '../S180_記憶が要る知らない_20261120'); import 数え
    return 数え.測る(900, 'v4', *x[:2], 寿命=1500, 差しかえ=x[2])
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a, b, c, d = p.map(f, [(False, None, False), (False, None, True), (True, None, True), (True, 'いない時', True)], chunksize=1)
    print('差しかえ・何もなし＝元の世界:', a == b, ' 隠すで変わる:', b != c, ' 漂いで変わる:', c != d)
