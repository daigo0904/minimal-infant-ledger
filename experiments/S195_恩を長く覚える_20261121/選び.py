import sys, numpy as np
sys.path.insert(0, '../S195_恩を長く覚える_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return 数え.測る(*job)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {x: np.array(p.map(one, [(s, x) for s in range(900, 910)], chunksize=1)) for x in [0.98, 0.998, 0.9995]}
    for x, r in R.items(): m = np.median(r, 0); print(f'恩薄れ{x}: 相関 {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 偏り（上位2人）{m[1]:.3f}')
    for x in [0.998, 0.9995]: print(f'{x} > 0.98：偏り {int((R[x][:,1] > R[0.98][:,1]).sum())}/10 相関 {int((R[x][:,0] > R[0.98][:,0]).sum())}/10')
