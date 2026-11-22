import sys, numpy as np
sys.path.insert(0, '../S246_語ごとの手応え_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, '分けて', 学び方=k)[:5]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in ['分けて', '両方']}
    for k, r in R.items(): print(f'学び方={k}: 組み立て度 {np.median(r[:,0]):.3f}・全体 {np.median(r[:,1]):.3f}・当たり {np.median(r[:,2]):.3f}・未見 {np.round(r[:,3],3).tolist()} 中央値 {np.median(r[:,3]):.3f}', flush=True)
    a, b = R['分けて'], R['両方']; print(f'未見 分けて>両方 {int((a[:,3] > b[:,3]).sum())}/10・未見>0.5 {int((a[:,3] > 0.5).sum())}/10・当たり 分けて>両方 {int((a[:,2] > b[:,2]).sum())}/10')
