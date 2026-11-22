import sys, json, numpy as np
sys.path.insert(0, '../S130_離れる長さと甘え_20261119')
from multiprocessing import Pool
from 共 import *
def one_(job): s, kD = job; return (s, kD) + tuple(float(x) for x in one((s, kD)))
if __name__ == '__main__':
    段 = sys.argv[1]; T = range(29400, 29430) if 段 == '本' else range(29500, 29530)
    with Pool(8) as p: r = p.map(one_, [(s, kD) for kD in [0.0, 30.0] for s in T])
    d = {(s, kD): v for s, kD, *v in r}
    res = {f'H1_{L_}手で戻って増える': int(sum(d[(s, 30.0)][j] > 0 for s in T)) for j, L_ in enumerate([250, 500, 1000])}
    res['H2_長いほど増える（1000>250）'] = int(sum(d[(s, 30.0)][2] > d[(s, 30.0)][0] for s in T))
    res['H3_長すぎると減る（500>1000）'] = int(sum(d[(s, 30.0)][1] > d[(s, 30.0)][2] for s in T))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kD{kD}': {f'{L_}手': round(float(np.median([d[(s, kD)][j] for s in T])), 3) for j, L_ in enumerate([250, 500, 1000])} for kD in [0.0, 30.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
