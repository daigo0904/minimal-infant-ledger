import json, numpy as np
from multiprocessing import Pool
import 頭 as H
def one(job):
    s, a = job
    if a is None: o = H.一生(s, '道具型')
    elif a == 'RLS': o = H.一生(s, '獲得型')
    else: H.歩幅[0] = a; o = H.一生(s, '獲得型', 遅く=True)
    f, g, _ = H.数字(o); return (s, a, f, g)
if __name__ == '__main__':
  腕 = [None, 'RLS', 0.001, 0.003, 0.01, 0.03]
  with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in range(900, 910)])
  d = {(s, a): (f, g) for s, a, f, g in r}
  for a in 腕[1:]:
    gap = [(d[(s, a)][0] - d[(s, None)][0], d[(s, a)][1] - d[(s, None)][1]) for s in range(900, 910)]
    print(a, '初め', round(np.median([d[(s, a)][0] for s in range(900, 910)]), 3), '育', round(np.median([d[(s, a)][1] for s in range(900, 910)]), 3),
          '差 初め', round(np.median([x[0] for x in gap]), 3), '差 育', round(np.median([x[1] for x in gap]), 3), '差が育つ', sum(x[1] > x[0] for x in gap))
  print('道具型', round(np.median([d[(s, None)][0] for s in range(900, 910)]), 3), round(np.median([d[(s, None)][1] for s in range(900, 910)]), 3))
