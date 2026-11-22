import sys, json, numpy as np
sys.path.insert(0, '../S155_物知りに会う回数_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 率, 正直 = job; o = 一生(s, '養育者', 'v4', 物知り=(1, 正直), 物知り率=率); return (s, 率, 正直) + 数える(o, 6000, 8000) + (o['sha256'],)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(33400, 33430) if 段 == '本' else range(33500, 33530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 率, 正直) for 率 in [None, 0.5] for 正直 in [1.0, 0.7, 0.5] for s in S], chunksize=1)
    d = {(s, 率, 正直): v for s, 率, 正直, *v in r}; assert len(d) == 180
    f = lambda s, 率, 正直: d[(s, 率, 正直)][1]
    比 = lambda s, 率: f(s, 率, 0.7) / max(f(s, 率, 1.0), 1e-9)
    res = {'H1_会えば学ぶ': sum(f(s, 0.5, 0.7) > f(s, None, 0.7) for s in S), 'H2_下げ方が緩む': sum(比(s, 0.5) > 比(s, None) for s in S),
           'H3_比例に届く': sum(f(s, 0.5, 0.7) >= 0.4 * f(s, 0.5, 1.0) for s in S), '対照_率0.5で0.7>0.5': sum(f(s, 0.5, 0.7) > f(s, 0.5, 0.5) for s in S),
           'sha違う_0.7': sum(d[(s, 0.5, 0.7)][4] != d[(s, None, 0.7)][4] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_会えば学ぶ', 'H2_下げ方が緩む', 'H3_比例に届く', '対照_率0.5で0.7>0.5']}
    res['中央値'] = {f'率{率}_{正直}': [round(float(np.median([d[(s, 率, 正直)][j] for s in S])), 3) for j in range(4)] for 率 in [None, 0.5] for 正直 in [1.0, 0.7, 0.5]}
    res['比の中央値'] = {f'率{率}': round(float(np.median([比(s, 率) for s in S])), 3) for 率 in [None, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
