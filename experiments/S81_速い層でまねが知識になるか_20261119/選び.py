import numpy as np
from multiprocessing import Pool
import 頭 as T
def one(job):
    s, k = job
    if k is None: o = T.一生(s, False)
    else: T.設定['kF'] = k; o = T.一生(s, True)
    return (s, k) + T.数(o)
if __name__ == '__main__':
    S = range(900, 910); K = [None, 1.0, 3.0, 10.0, 30.0]
    with Pool(8) as p: r = p.map(one, [(s, k) for k in K for s in S])
    d = {(s, k): (a, b, c) for s, k, a, b, c in r}
    for k in K:
        print('なし' if k is None else k, '乗り換え', round(float(np.median([d[(s, k)][0] for s in S])), 3), 'お手本以外が見る時の当たり', round(float(np.median([d[(s, k)][1] for s in S])), 3),
              'お手本が見る時の当たり', round(float(np.median([d[(s, k)][2] for s in S])), 3), ('' if k is None else f"広がり>なし {sum(d[(s, k)][1] > d[(s, None)][1] for s in S)}/10"))
