import numpy as np
from multiprocessing import Pool
import 頭 as H
if __name__ == '__main__':
    a = H.一生(999, False, 600); b = H.一生(999, True, 600); print('合図あり≠なし:', a['sha256'] != b['sha256'])
    with Pool(8) as p: r = p.map(H.one, [(s, k) for k in [False, True] for s in range(900, 910)])
    for k in [False, True]:
        print('合図' + ('あり' if k else 'なし'), '育った後 P養/P他/差 中央値:', [round(float(np.median([x[3][j] for x in r if x[1] == k])), 3) for j in range(3)])
