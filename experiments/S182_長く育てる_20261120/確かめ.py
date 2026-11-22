import sys
from multiprocessing import Pool
def f(x):
    sys.path.insert(0, '../S182_長く育てる_20261120'); import 数え; return 数え.測る(900, 0.5, 寿命=8000)
def g(x):
    sys.path.insert(0, '../S181_記憶を足す_20261120'); import 数え; r = 数え.測る(900, 'v4', True, 'いない時', 記憶=0.5); return r
if __name__ == '__main__':
    with Pool(2, maxtasksperchild=1) as p: a = p.map(f, [0])[0]; b = p.map(g, [0])[0]
    print('寿命8000 で S181 と同じ手:', a[-1] == b[-1], ' 6000〜8000 の指す差 同じ:', abs(a[0] - b[0]) < 1e-12, round(a[0], 4), round(b[0], 4))
