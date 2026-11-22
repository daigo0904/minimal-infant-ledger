import sys, numpy as np
sys.path.insert(0, '../S178_生まれつきの自分の好み_20261120')
from multiprocessing import Pool
from 共 import 一生, ブロッコリー
def one(job): s, k = job; o = 一生(s, 'v4', 二人=0.5, 自分=0.05, k生まれ=k); return np.array([ブロッコリー(o, lo, lo + 1000) for lo in range(0, 8000, 1000)])
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for k in [0.1, 0.3, 1.0]:
            r = np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'生まれつき{k}: B の前の差 ' + ' '.join(f'{v:+.2f}' for v in m[:, 0]) + ' ／ 仲間の前の自分好き ' + ' '.join(f'{v:.2f}' for v in m[:, 1]), flush=True)
            print(f'   初め<0 {int((r[:, 0, 0] < 0).sum())}/10  終わり>0 {int((r[:, 7, 0] > 0).sum())}/10  切り替わる {int(((r[:, 0, 0] < 0) & (r[:, 7, 0] > 0)).sum())}/10', flush=True)
