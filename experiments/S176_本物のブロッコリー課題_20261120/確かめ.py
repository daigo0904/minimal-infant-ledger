import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S176_本物のブロッコリー課題_20261120'); import 共; o = 共.一生(900, 'v4', 1500, 二人=0.5, 自分=x); return o['sha256'], o['自分手'], o['一番'], o['一番B']
def 旧(_):
    sys.path.insert(0, '../S175_相手ごとの好み_20261120'); import 共; return 共.一生(900, 'v4', 1500, 二人=0.5)['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: (a, *_), (b, 自, a1, b1) = p.map(新, [None, 0.05], chunksize=1); c = p.map(旧, [0])[0]
    print('自分なし＝S175:', a == c, ' 自分で変わる:', a != b, ' A好き', a1, 'B好き', b1, '自分好き', 自)
