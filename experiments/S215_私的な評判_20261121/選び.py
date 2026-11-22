import sys, numpy as np
sys.path.insert(0, '../S215_私的な評判_20261121')
from multiprocessing import Pool
腕 = {'共有評判': (5.0, False), '私的評判': (5.0, True), '評判なし': (0.0, False)}
def one(job):
    import 数え; s, 名 = job; ρ, 私 = 腕[名]; return 数え.測る(s, ρ=ρ, 私的=私)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 得（親切でない−親切の空腹）{np.round(r[:,0], 3).tolist()} 中央値 {np.median(r[:,0]):+.4f}（>0 {int((r[:,0]>0).sum())}/10）・空腹 親切 {np.median(r[:,1]):.3f} 親切でない {np.median(r[:,2]):.3f}', flush=True)
    a, b, c = R['私的評判'][:,0], R['評判なし'][:,0], R['共有評判'][:,0]; print(f'私的>評判なし {int((a > b).sum())}/10・私的<共有 {int((a < c).sum())}/10')
