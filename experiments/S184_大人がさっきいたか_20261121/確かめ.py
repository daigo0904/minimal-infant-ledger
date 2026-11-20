import sys, importlib.util
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S184_大人がさっきいたか_20261121'); import 数え; return 数え.長く(900, 0.5, '両方', 寿命=1500, 気づく=x)
def 旧(_):
    sys.path.insert(0, '../S183_記憶のどこが効くか_20261120'); import 数え; return 数え.長く(900, 0.5, '両方', 寿命=1500)
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [False, True], chunksize=1); c = p.map(旧, [0])[0]
    print('気づくなし＝S183:', a == c, ' 気づくで変わる:', a != b)
