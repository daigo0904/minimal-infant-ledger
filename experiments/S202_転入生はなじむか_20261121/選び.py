import sys, numpy as np
sys.path.insert(0, '../S202_転入生はなじむか_20261121')
from multiprocessing import Pool
def one(s):
    import 数え; return 数え.測る(s)[:6]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: r = np.array(p.map(one, range(900, 910), chunksize=1))
    m = np.median(r, 0); print('なぐさめてもらった差 0〜1000／1000〜2000／2000〜3000:', ' '.join(f'{v:+.0f}' for v in m[:3]), ' 入り次数の差:', ' '.join(f'{v:+.2f}' for v in m[3:]))
    print('縮む（2000〜3000 > 0〜1000）なぐさめ', int((r[:,2] > r[:,0]).sum()), '/10 入り次数', int((r[:,5] > r[:,3]).sum()), '/10  2000〜3000 でもまだ不利（<0）', int((r[:,2] < 0).sum()), '/10')
