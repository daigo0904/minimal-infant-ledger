import numpy as np
from multiprocessing import Pool
import 頭 as T
def one(job):
    s, v, a, 腕, e = job; T.率.update(V=v, A=a); o = T.一生(s, 腕, e); return (s, v, a, 腕, e) + T.数(o, e)
if __name__ == '__main__':
    S = range(900, 910); 組 = [(0.05, 0.01), (0.02, 0.01), (0.1, 0.01)]
    with Pool(8) as p: r = p.map(one, [(s, v, a, 'V+A', e) for v, a in 組 for e in [False, True] for s in S] + [(s, 0, 0, 'Q', e) for e in [False, True] for s in S])
    d = {(s, v, a, w, e): (x, y) for s, v, a, w, e, x, y in r}
    base = {s: d[(s, 0, 0, 'Q', False)][1] for s in S}
    print('元 Q: 戻り差', round(np.median([d[(s, 0, 0, 'Q', True)][0] - d[(s, 0, 0, 'Q', False)][0] for s in S]), 3), '見られ分け', round(np.median(list(base.values())), 3))
    for v, a in 組:
        inc = [d[(s, v, a, 'V+A', True)][0] - d[(s, v, a, 'V+A', False)][0] for s in S]
        print(v, a, '戻り差', round(float(np.median(inc)), 3), '増えた数', sum(x > 0 for x in inc), '見られ分け', round(float(np.median([d[(s, v, a, 'V+A', False)][1] for s in S])), 3), '0.9倍以上', sum(d[(s, v, a, 'V+A', False)][1] >= 0.9 * base[s] for s in S))
