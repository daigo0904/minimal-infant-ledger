import numpy as np
from multiprocessing import Pool
import 頭 as H
def one(job):
    s, k, C = job
    if k is None: o = H.一生(s, False)
    else: H.記憶.設定.update(kD=k, 容量=C); o = H.一生(s, True)
    return (s, k, C) + H.数(o)
if __name__ == '__main__':
    S = range(900, 910); G = [(None, 0), (30.0, 300), (100.0, 300), (10.0, 100), (30.0, 100)]
    with Pool(8) as p: r = p.map(one, [(s, k, C) for k, C in G for s in S])
    d = {(s, k, C): (a, b, c) for s, k, C, a, b, c in r}
    for k, C in G:
        print('一層' if k is None else (k, C), '乗り換え', round(float(np.median([d[(s, k, C)][0] for s in S])), 3), 'お手本以外が見る時の当たり', round(float(np.median([d[(s, k, C)][1] for s in S])), 3),
              'お手本が見る時', round(float(np.median([d[(s, k, C)][2] for s in S])), 3), '' if k is None else f"一層より大 {sum(d[(s, k, C)][1] > d[(s, None, 0)][1] for s in S)}/10")
