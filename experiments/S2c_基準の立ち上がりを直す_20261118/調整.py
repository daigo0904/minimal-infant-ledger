import sys, numpy as np
import 世界 as W
for s in [int(x) for x in sys.argv[1:]]:
    for w in W.世界の種類:
        for h in W.頭の種類:
            o = W.一生(s, w, h); AD, 喜, 差 = W.区間の数字(o)
            f = lambda v: [round(x, 2) for x in v[::2]]
            print(s, w, h, '見られ分け差', f(差), '喜', f(喜), '空腹', round(float(o['h列'].mean()), 2), flush=True)
