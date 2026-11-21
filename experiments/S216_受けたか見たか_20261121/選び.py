import sys, numpy as np
sys.path.insert(0, '../S216_受けたか見たか_20261121')
from multiprocessing import Pool
腕 = {'両方': (5.0, True), '受けた分だけ': (5.0, '受けた'), '見た分だけ': (5.0, '見た'), '評判なし': (0.0, False)}
def one(job):
    import 数え; s, 名 = job; ρ, 私 = 腕[名]; return 数え.測る(s, ρ=ρ, 私的=私)[:3]
def 回数(s):
    import 数え; A = 数え.一生(s, 5.0, True, (0, 1, 2, 3), 4000)['相手列']; 受 = 見 = 0
    for i in range(8):
        for j in range(8):
            if i != j: u = A[:, j] == i + 1; 受 += u.mean(); 見 += ((A[:, i] == j + 1) & ~u).mean()
    return 受 / 56, 見 / 56
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        print('1組あたり1手の回数（受けた・見た）', np.round(p.map(回数, [900, 901]), 4).tolist(), flush=True)
        R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 得 {np.round(r[:,0], 3).tolist()} 中央値 {np.median(r[:,0]):+.4f}（>0 {int((r[:,0]>0).sum())}/10）・空腹 親切 {np.median(r[:,1]):.3f} 親切でない {np.median(r[:,2]):.3f}', flush=True)
    a, b = R['受けた分だけ'][:,0], R['見た分だけ'][:,0]; print(f'受けた>見た {int((a > b).sum())}/10・受けた>なし {int((a > R["評判なし"][:,0]).sum())}/10・見た>なし {int((b > R["評判なし"][:,0]).sum())}/10')
