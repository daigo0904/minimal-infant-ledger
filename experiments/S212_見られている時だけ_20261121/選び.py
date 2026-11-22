import sys, numpy as np
sys.path.insert(0, '../S212_見られている時だけ_20261121')
from multiprocessing import Pool
腕 = {'観客入力・見られ評判': (True, True), '観客入力・いつも評判': (True, False), '入力なし・見られ評判': (False, True)}
def one(job):
    import 数え; s, 名 = job; 観, 見評 = 腕[名]; return 数え.測る(s, 1.0, β=0.0, 親切=3.0, ρ=5.0, 観=観, 見評=見評)[:6]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 親切 終わり 中央値 {np.median(r[:,0]):.2f}（>4 {int((r[:,0]>4).sum())}/10）・同じ子の中の差 {np.round(r[:,1], 3).tolist()} 中央値 {np.median(r[:,1]):+.4f}（>0 {int((r[:,1]>0).sum())}/10）・混ぜた差 {np.median(r[:,2]):+.3f}・観客ありの割合 {np.median(r[:,5]):.2f}', flush=True)
    a, b = R['観客入力・見られ評判'], R['観客入力・いつも評判']; c = R['入力なし・見られ評判']; print(f'同じ子の中の差 見られ評判 > いつも評判 {int((a[:,1] > b[:,1]).sum())}/10・入力あり > 入力なし {int((a[:,1] > c[:,1]).sum())}/10')
