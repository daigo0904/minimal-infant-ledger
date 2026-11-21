import sys, numpy as np
sys.path.insert(0, '../S236_分けて聞く_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:5]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in ['分けて', 'まとめて']}
    for k, r in R.items(): print(f'{k}: 組み立て度 中央値 {np.median(r[:,0]):.3f}・全体 {np.median(r[:,1]):.3f}・当たり {np.median(r[:,2]):.3f}・未見（最初1000）{np.round(r[:,3],3).tolist()} 中央値 {np.median(r[:,3]):.3f}', flush=True)
    a, b = R['分けて'], R['まとめて']; print(f'組み立て 分けて>まとめて {int((a[:,0] > b[:,0]).sum())}/10・未見>3/16 {int((a[:,3] > 3/16).sum())}/10・未見 分けて>まとめて {int((a[:,3] > b[:,3]).sum())}/10')
