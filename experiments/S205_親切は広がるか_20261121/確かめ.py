import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S205_親切は広がるか_20261121'); import 数え; return 数え.測る(900, 選=x, 寿命=1500)
def 旧(_):
    sys.path.insert(0, '../S204_親切の見返り_20261121'); import 数え; return 数え.測る(900, 3.0, 寿命=1500)
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [None, (700, 200)], chunksize=1); c = p.map(旧, [0])[0]
    print('入れ替えなし＝S204（親切3）:', a == c, ' 選び替えで変わる:', a != b)
