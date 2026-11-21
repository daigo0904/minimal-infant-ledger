import sys, numpy as np
sys.path.insert(0, '../S220_嘘を見抜く_20261121')
from multiprocessing import Pool
腕 = {'嘘つき・信用なし': (True, False), '嘘つき・信用あり': (True, True), '嘘つきなし・信用なし': (False, False)}
def one(job):
    import 数え; s, 名 = job; u, c = 腕[名]; return 数え.測る(s, 嘘=u, 信用=c)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 得 中央値 {np.median(r[:,0]):+.4f}・表の相関 {np.median(r[:,1]):.3f}・嘘つきへの信用 {np.median(r[:,2]):.3f}・正直への信用 {np.median(r[:,3]):.3f}', flush=True)
    a, b = R['嘘つき・信用あり'], R['嘘つき・信用なし']; print(f'信用で得が戻る {int((a[:,0] > b[:,0]).sum())}/10・相関が戻る {int((a[:,1] > b[:,1]).sum())}/10・嘘つき信用<正直 {int((a[:,2] < a[:,3]).sum())}/10')
