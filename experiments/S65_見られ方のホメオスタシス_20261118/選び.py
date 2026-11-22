import numpy as np
from multiprocessing import Pool
import 頭 as H
def one(job):
    s, 目標, k, 欠 = job; H.設定['目標'] = 目標; H.設定['k'] = k
    o = H.一生(s, 'あり', 欠); return (s, 目標, k, 欠) + H.数(o)
def base(job):
    s, 欠 = job; o = H.一生(s, 'なし', 欠); return (s, 欠) + H.数(o)
if __name__ == '__main__':
    S = range(900, 910); 組 = [(0.2, 1.0), (0.3, 1.0), (0.3, 3.0), (0.5, 3.0)]
    with Pool(8) as p:
        r = p.map(one, [(s, g, k, e) for g, k in 組 for e in [False, True] for s in S]); b = p.map(base, [(s, e) for e in [False, True] for s in S])
    db = {(s, e): (x, y) for s, e, x, y in b}
    print('なし: 戻り差', round(np.median([db[(s, True)][0] - db[(s, False)][0] for s in S]), 3), '見られ分け', round(np.median([db[(s, False)][1] for s in S]), 3))
    for g, k in 組:
        d = {(s, e): (x, y) for s, gg, kk, e, x, y in r if gg == g and kk == k}
        print(g, k, '戻り差', round(np.median([d[(s, True)][0] - d[(s, False)][0] for s in S]), 3), '増えた数', sum(d[(s, True)][0] > d[(s, False)][0] for s in S),
              '見られ分け', round(np.median([d[(s, False)][1] for s in S]), 3), '0.9倍以上', sum(d[(s, False)][1] >= 0.9 * db[(s, False)][1] for s in S))
