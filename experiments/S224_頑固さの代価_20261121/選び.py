import sys, numpy as np
sys.path.insert(0, '../S224_頑固さの代価_20261121')
from multiprocessing import Pool
腕 = {'噂なし': (0.0, None), '噂のみ': (0.05, None), '噂＋ふるい': (0.05, 0.05)}
def one(job):
    import 数え; s, 名 = job; g, f = 腕[名]; return 数え.測る(s, 噂=g, ふるい=f)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 追いつく手数 {r[:,0].tolist()} 中央値 {np.median(r[:,0]):.0f}・変わる子の空腹 {np.median(r[:,1]):.3f}・評判の上がり {np.median(r[:,2]):+.3f}', flush=True)
    a, b, c = R['噂＋ふるい'], R['噂のみ'], R['噂なし']; print(f'ふるい>噂のみ（遅い）{int((a[:,0] > b[:,0]).sum())}/10・ふるい>噂なし {int((a[:,0] > c[:,0]).sum())}/10・空腹 ふるい>噂のみ {int((a[:,1] > b[:,1]).sum())}/10')
