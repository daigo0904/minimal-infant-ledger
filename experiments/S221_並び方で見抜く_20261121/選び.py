import sys, numpy as np
sys.path.insert(0, '../S221_並び方で見抜く_20261121')
from multiprocessing import Pool
腕 = {'嘘つき・差の信用': (True, True), '嘘つき・並びの信用': (True, '並び'), '嘘つきなし': (False, False)}
def one(job):
    import 数え; s, 名 = job; u, c = 腕[名]; return 数え.測る(s, 嘘=u, 信用=c)[:4]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 得 中央値 {np.median(r[:,0]):+.4f}・表の相関 {np.median(r[:,1]):.3f}・嘘つきへの信用 {np.median(r[:,2]):.3f}・正直への信用 {np.median(r[:,3]):.3f}', flush=True)
    a, b, n = R['嘘つき・並びの信用'], R['嘘つき・差の信用'], R['嘘つきなし']; print(f'並びで嘘つき信用<差 {int((a[:,2] < b[:,2]).sum())}/10・得 並び>差 {int((a[:,0] > b[:,0]).sum())}/10・得 並び≥嘘つきなし {int((a[:,0] >= n[:,0]).sum())}/10・正直への信用>0.5 {int((a[:,3] > 0.5).sum())}/10')
