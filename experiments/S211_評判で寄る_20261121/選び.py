import sys, numpy as np
sys.path.insert(0, '../S211_評判で寄る_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, β, k, ρ = job; return 数え.測る(s, 1.0, β=β, 親切=k, ρ=ρ)[:2]
if __name__ == '__main__':
    腕 = [(0.0, 3.0, 5.0), (0.0, 1.0, 5.0), (0.3, 3.0, 5.0), (0.3, 1.0, 5.0)]
    with Pool(8, maxtasksperchild=1) as p: R = {a: np.array(p.map(one, [(s,) + a for s in range(900, 910)], chunksize=1)) for a in 腕}
    for a, r in R.items(): print(f'β{a[0]} 親切{a[1]} ρ{a[2]}: 終わり {np.round(r[:,0], 1).tolist()}（中央値 {np.median(r[:,0]):.2f}、0 の世界 {int((r[:,0]==0).sum())}）', flush=True)
    for β in [0.0, 0.3]: a, c = R[(β, 3.0, 5.0)], R[(β, 1.0, 5.0)]; print(f'β{β}：親切>対照 {int((a[:,0] > c[:,0]).sum())}/10 親切<対照 {int((a[:,0] < c[:,0]).sum())}/10 親切>4 {int((a[:,0] > 4).sum())}/10')
