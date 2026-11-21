import sys, numpy as np
sys.path.insert(0, '../S228_二人だけの言葉_20261121')
from multiprocessing import Pool
腕 = ['毎回', '固定', '固定・役交代']
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in 腕}
    for k, r in R.items(): print(f'{k}: 当たり 中央値 {np.median(r[:,0]):.3f}・全体の結びつき {np.median(r[:,1]):.3f}・話し手ごとの結びつき {np.median(r[:,2]):.3f}', flush=True)
    a, b, c = R['毎回'], R['固定'], R['固定・役交代']
    print(f'固定>毎回 全体 {int((b[:,1] > a[:,1]).sum())}/10・当たり {int((b[:,0] > a[:,0]).sum())}/10｜役交代>毎回 当たり {int((c[:,0] > a[:,0]).sum())}/10・全体 {int((c[:,1] > a[:,1]).sum())}/10・話し手ごと {int((c[:,2] > a[:,2]).sum())}/10')
