import numpy as np, time
from multiprocessing import Pool
import 頭 as H
def one(job):
    s, k = job
    if k is None: o = H.一生(s, False)
    else: H.記憶.設定['kD'] = k; o = H.一生(s, True)
    return (s, k) + H.数(o)
if __name__ == '__main__':
    t = time.time(); H.一生(999, True, 寿命=500); print('500手の時間', round(time.time() - t, 1), '秒')
    S = range(900, 910); K = [None, 1.0, 3.0, 10.0]
    with Pool(8) as p: r = p.map(one, [(s, k) for k in K for s in S])
    d = {(s, k): (a, b, c) for s, k, a, b, c in r}
    for k in K:
        print('一層' if k is None else k, '乗り換え', round(float(np.median([d[(s, k)][0] for s in S])), 3), 'お手本以外が見る時の当たり', round(float(np.median([d[(s, k)][1] for s in S])), 3),
              'お手本が見る時', round(float(np.median([d[(s, k)][2] for s in S])), 3), '' if k is None else f"一層より大 {sum(d[(s, k)][1] > d[(s, None)][1] for s in S)}/10")
