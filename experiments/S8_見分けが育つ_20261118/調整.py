import sys, numpy as np, 世界S8 as X, 世界 as W
def 分け(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    return float(np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() - (A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)]))
for s in [int(x) for x in sys.argv[1:]]:
    for 種類 in ['育つ', '固定']:
        o = X.一生(s, '獲得型', 種類, 寿命=8000, 離乳=8000)
        print(s, 種類, [round(分け(o, k, k + 500), 3) for k in range(0, 8000, 1000)], flush=True)
