import sys, numpy as np
sys.path.insert(0, '../S227_言葉が要る世界_20261121')
from multiprocessing import Pool
腕 = {'本（共感・聞き手は見えない）': (50.0, False), '聞き手も見える': (50.0, True), '共感なし': (0.0, False)}
def one(job):
    import 数え; s, 名 = job; k, v = 腕[名]; return 数え.測る(s, k, v)[:3]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: R = {名: np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)) for 名 in 腕}
    for 名, r in R.items(): print(f'{名}: 当たり {np.round(r[:,0], 3).tolist()} 中央値 {np.median(r[:,0]):.3f}・合図と場所の結びつき {np.round(r[:,1], 3).tolist()} 中央値 {np.median(r[:,1]):.3f}ビット・空腹 {np.median(r[:,2]):.3f}', flush=True)
    a, b, c = R['本（共感・聞き手は見えない）'], R['聞き手も見える'], R['共感なし']
    print(f'当たり>0.30 {int((a[:,0] > 0.30).sum())}/10・結びつき 本>見える {int((a[:,1] > b[:,1]).sum())}/10・本>共感なし {int((a[:,1] > c[:,1]).sum())}/10・当たり 本>共感なし {int((a[:,0] > c[:,0]).sum())}/10')
