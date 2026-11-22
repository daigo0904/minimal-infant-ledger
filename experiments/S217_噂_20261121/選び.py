import sys, numpy as np
sys.path.insert(0, '../S217_噂_20261121')
from multiprocessing import Pool
腕 = {'見た・噂なし': (5.0, '見た', 0.0), '見た・噂0.01': (5.0, '見た', 0.01), '見た・噂0.05': (5.0, '見た', 0.05), '共有': (5.0, False, 0.0)}
def one(job):
    import 数え; s, 名 = job; ρ, 私, g = 腕[名]; return 数え.測る(s, ρ=ρ, 私的=私, 噂=g)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 得 中央値 {np.median(r[:,0]):+.4f}（>0 {int((r[:,0]>0).sum())}/10）・表の相関 中央値 {np.nanmedian(r[:,1]):+.3f}', flush=True)
    n, c = R['見た・噂なし'], R['共有']
    for g in ['見た・噂0.01', '見た・噂0.05']:
        a = R[g]; print(f'{g}: 得>噂なし {int((a[:,0] > n[:,0]).sum())}/10・|共有−噂| < |共有−噂なし| {int((abs(c[:,0]-a[:,0]) < abs(c[:,0]-n[:,0])).sum())}/10・相関>噂なし {int((a[:,1] > n[:,1]).sum())}/10')
