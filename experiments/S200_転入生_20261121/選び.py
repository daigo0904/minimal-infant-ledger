import sys, numpy as np
sys.path.insert(0, '../S200_転入生_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, γ, 転 = job; return 数え.測る(s, γ, 転入=転)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        R = {(γ, 転): np.array(p.map(one, [(s, γ, 転) for s in range(900, 910)], chunksize=1)) for γ in [0.0, 5.0] for 転 in [None, 4000]}
    for (γ, 転), r in R.items(): m = np.median(r, 0); print(f'γ{γ} 転入{転}: 子0 の入り次数 {m[0]:.1f}（他の平均 {m[1]:.2f}、0 の世界 {int((r[:,0]==0).sum())}/10） 空腹差 {m[2]:+.3f} なぐさめてもらった差 {m[3]:+.0f}')
    for γ in [0.0, 5.0]: a, b = R[(γ, 4000)], R[(γ, None)]; print(f'γ{γ}：転入生の空腹差 > 入れ替えなし {int((a[:,2] > b[:,2]).sum())}/10  なぐさめてもらった差 < 入れ替えなし {int((a[:,3] < b[:,3]).sum())}/10')
    a, b = R[(5.0, 4000)], R[(0.0, 4000)]; print('転入生 γ5 vs γ0：空腹差が小さい', int((a[:,2] < b[:,2]).sum()), '/10 なぐさめてもらった差が大きい', int((a[:,3] > b[:,3]).sum()), '/10 入り次数が多い', int((a[:,0] > b[:,0]).sum()), '/10')
