import sys, numpy as np
sys.path.insert(0, '../S229_自分の耳で話す_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in ['ふつう', '耳']}
    for k, r in R.items(): print(f'{k}: 当たり {np.round(r[:,0],3).tolist()} 中央値 {np.median(r[:,0]):.3f}・全体の結びつき 中央値 {np.median(r[:,1]):.3f}・話し手ごと {np.median(r[:,2]):.3f}・言い方の一致 {np.round(r[:,3],2).tolist()} 中央値 {np.median(r[:,3]):.3f}', flush=True)
    a, b = R['耳'], R['ふつう']; print(f'耳>ふつう 全体 {int((a[:,1] > b[:,1]).sum())}/10・当たり {int((a[:,0] > b[:,0]).sum())}/10・一致 {int((a[:,3] > b[:,3]).sum())}/10')
