import numpy as np
from multiprocessing import Pool
import 頭 as H
def one(job):
    s, a = job
    if a == '道具': o = H.一生(s, '道具型')
    elif a == '元': o = H.一生(s, '獲得型')
    else: H.c[0] = a; o = H.一生(s, '獲得型', 換算する=True)
    return (s, a) + H.数字(o)
if __name__ == '__main__':
    S = range(900, 910); 腕 = ['道具', '元', 3.0, 10.0, 30.0, 100.0]
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): (f, g) for s, a, f, g in r}
    for a in 腕[1:]:
        gap = [(d[(s, a)][0] - d[(s, '道具')][0], d[(s, a)][1] - d[(s, '道具')][1]) for s in S]
        print(a, '初め', round(np.median([d[(s, a)][0] for s in S]), 3), '育', round(np.median([d[(s, a)][1] for s in S]), 3),
              '差 初め→育', round(np.median([x[0] for x in gap]), 3), round(np.median([x[1] for x in gap]), 3), '差が育つ', sum(x[1] > x[0] for x in gap),
              '育ち', sum(d[(s, a)][0] <= d[(s, a)][1] / 2 for s in S))
    print('道具', round(np.median([d[(s, '道具')][0] for s in S]), 3), round(np.median([d[(s, '道具')][1] for s in S]), 3))
