import sys, numpy as np
sys.path.insert(0, '../S218_なぜ得が増えないか_20261121')
from multiprocessing import Pool
腕 = {'噂なし': ('見た', 0.0), '噂0.01': ('見た', 0.01), '共有': (False, 0.0)}
名前 = ['a_親切へ寄る割合', '受けた_親切', '受けた_親切でない', '受けた差', '親→親', '親→不', '不→親', '不→不', '得']
def one(job):
    import 数え; s, 名 = job; 私, g = 腕[名]; return 数え.測る(s, 私的=私, 噂=g)[:9]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(名, '　'.join(f'{n} {v:.4f}' for n, v in zip(名前, np.median(r, 0))), flush=True)
    n, g = R['噂なし'], R['噂0.01']; print(f"噂0.01：(a)>噂なし {int((g[:,0] > n[:,0]).sum())}/10・受けた差>噂なし {int((g[:,3] > n[:,3]).sum())}/10・受けた_親切でない>噂なし {int((g[:,2] > n[:,2]).sum())}/10・親→親>噂なし {int((g[:,4] > n[:,4]).sum())}/10")
