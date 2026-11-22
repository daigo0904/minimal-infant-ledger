import numpy as np
from multiprocessing import Pool
import 頭 as T
def one(job):
    s, gg, e = job; o = T.一生(s, gg, e); return (s, gg, e) + T.数(o, e)
if __name__ == '__main__':
    S = range(900, 910); G = [0.0, 1.0, 3.0, 10.0]
    with Pool(8) as p: r = p.map(one, [(s, gg, e) for gg in G for e in [False, True] for s in S])
    d = {(s, gg, e): (x, y) for s, gg, e, x, y in r}
    for gg in G:
        inc = [d[(s, gg, True)][0] - d[(s, gg, False)][0] for s in S]
        print(gg, '戻り差', round(float(np.median(inc)), 3), '増えた数', sum(x > 0 for x in inc), '見られ分け', round(float(np.median([d[(s, gg, False)][1] for s in S])), 3), '0.9倍以上', sum(d[(s, gg, False)][1] >= 0.9 * d[(s, 0.0, False)][1] for s in S))
