import sys, numpy as np
sys.path.insert(0, '../S232_文化の継承_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in ['耳', 'ふつう']}
    for k, r in R.items(): print(f'{k}: 最初の言葉との一致 {r[:,0].tolist()}・最後の当たり 中央値 {np.median(r[:,1]):.3f}・最後のそろい {np.median(r[:,2]):.3f}', flush=True)
    a, b = R['耳'], R['ふつう']; print(f'耳で一致1.0 {int((a[:,0] == 1.0).sum())}/10・耳>ふつう {int((a[:,0] > b[:,0]).sum())}/10・耳で当たり>0.7 {int((a[:,1] > 0.7).sum())}/10')
