import sys, numpy as np
sys.path.insert(0, '../S242_食べ予測を止める_20261122')
from multiprocessing import Pool
腕 = {'kf3・kE50': (3.0, 50.0, True), 'kf3・kE500': (3.0, 500.0, True), 'kf0・kE50': (0.0, 50.0, True), 'kf0・kE500': (0.0, 500.0, True), '協力・kf0・kE500': (0.0, 500.0, False), '協力・kf3・kE50': (3.0, 50.0, False)}
def one(job):
    import 数え; s, 名 = job; kf, kE, c = 腕[名]; return 数え.測る(s, kf, kE, c)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 当たり 中央値 {np.median(r[:,0]):.3f}・全体 {np.median(r[:,1]):.3f}・話し手ごと {np.median(r[:,2]):.3f}', flush=True)
    a, b, c = R['kf0・kE500'], R['kf3・kE500'], R['kf0・kE50']
    print(f'kf0kE500>kf3kE500 {int((a[:,0] > b[:,0]).sum())}/10・kf0kE500>0.30 {int((a[:,0] > 0.30).sum())}/10・kf0 kE500>kE50 {int((a[:,0] > c[:,0]).sum())}/10')
