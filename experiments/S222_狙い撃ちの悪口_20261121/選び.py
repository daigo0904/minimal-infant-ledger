import sys, numpy as np
sys.path.insert(0, '../S222_狙い撃ちの悪口_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, 悪 = job; return 数え.測る(s, 悪=悪)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {v: np.array(p.map(one, [(s, v) for s in range(900, 910)], chunksize=1)) for v in [True, False]}
    for v, r in R.items(): print(f'悪口={v}: 標的の損 {np.round(r[:,0], 3).tolist()} 中央値 {np.median(r[:,0]):+.4f}（>0 {int((r[:,0]>0).sum())}/10）・嘘つきへの信用 {np.median(r[:,1]):.3f}・正直への信用 {np.median(r[:,2]):.3f}・標的の評判差 {np.median(r[:,3]):+.3f}', flush=True)
    a, b = R[True], R[False]; print(f'標的の損 悪口>なし {int((a[:,0] > b[:,0]).sum())}/10・嘘つきへの信用>0.5 {int((a[:,1] > 0.5).sum())}/10・標的の評判 悪口<なし {int((a[:,3] < b[:,3]).sum())}/10')
