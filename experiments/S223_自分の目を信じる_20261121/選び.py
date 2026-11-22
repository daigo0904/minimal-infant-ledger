import sys, numpy as np
sys.path.insert(0, '../S223_自分の目を信じる_20261121')
from multiprocessing import Pool
腕 = {'悪口・ふるいなし': (True, None, 0.05), '悪口・ふるい0.05': (True, 0.05, 0.05), '悪口・ふるい0.1': (True, 0.1, 0.05), '悪口なし・ふるい0.05': (False, 0.05, 0.05), '悪口なし・ふるい0.1': (False, 0.1, 0.05), '悪口なし・噂なし': (False, None, 0.0)}
def one(job):
    import 数え; s, 名 = job; a, f, g = 腕[名]; return 数え.測る(s, 悪=a, ふるい=f, 噂=g)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 標的の損 {np.median(r[:,0]):+.4f}・嘘つきへの信用 {np.median(r[:,1]):.3f}・標的の評判差 {np.median(r[:,2]):+.3f}・表の相関 {np.median(r[:,3]):.3f}', flush=True)
    n = R['悪口・ふるいなし']; z = R['悪口なし・噂なし']
    for τ in ['0.05', '0.1']:
        a, b = R[f'悪口・ふるい{τ}'], R[f'悪口なし・ふるい{τ}']; print(f'τ{τ}: 標的の損が減る {int((a[:,0] < n[:,0]).sum())}/10・評判差が戻る {int((a[:,2] > n[:,2]).sum())}/10・悪口なしで相関 ≥ 噂なし {int((b[:,3] >= z[:,3]).sum())}/10')
