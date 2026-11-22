import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S185_見られ分けの余韻_20261121'); import 共; return 共.一生(900, 'v4', 1500, 記憶=x)['sha256']
def 旧(_):
    sys.path.insert(0, '../S175_相手ごとの好み_20261120'); import 共; return 共.一生(900, 'v4', 1500)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [None, 0.5], chunksize=1); c = p.map(旧, [0])[0]
    print('記憶なし＝S175（＝S152 48）:', a == c, a[:8], ' 記憶で変わる:', a != b)
