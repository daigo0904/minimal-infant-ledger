import sys, numpy as np
sys.path.insert(0, '../S219_嘘つきの噂_20261121')
from multiprocessing import Pool
腕 = {'噂・嘘つきなし': (0.05, False), '噂・嘘つき1人': (0.05, True), '噂なし': (0.0, False)}
def one(job):
    import 数え; s, 名 = job; g, u = 腕[名]; return 数え.測る(s, 噂=g, 嘘=u)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 得 中央値 {np.median(r[:,0]):+.4f}（>0 {int((r[:,0]>0).sum())}/10）・表の相関 中央値 {np.median(r[:,1]):+.3f}', flush=True)
    a, b, c = R['噂・嘘つき1人'], R['噂・嘘つきなし'], R['噂なし']; print(f'嘘で得が減る {int((a[:,0] < b[:,0]).sum())}/10・嘘で相関が下がる {int((a[:,1] < b[:,1]).sum())}/10・嘘つき<噂なし {int((a[:,0] < c[:,0]).sum())}/10')
