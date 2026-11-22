import sys, numpy as np
sys.path.insert(0, '../S230_言葉の習得_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, k)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {k: np.array(p.map(one, [(s, k) for s in range(900, 910)], chunksize=1)) for k in ['耳', 'ふつう']}
    for k, r in R.items(): print(f'{k}: 新入りの当たり 来てすぐ {np.median(r[:,0]):.3f} 最後 {np.median(r[:,1]):.3f}（後>前 {int((r[:,1] > r[:,0]).sum())}/10）・言い方の一致 {r[:,2].tolist()} 中央値 {np.median(r[:,2]):.2f}', flush=True)
    print(f'一致 耳>ふつう {int((R["耳"][:,2] > R["ふつう"][:,2]).sum())}/10・耳で一致>0.5 {int((R["耳"][:,2] > 0.5).sum())}/10')
