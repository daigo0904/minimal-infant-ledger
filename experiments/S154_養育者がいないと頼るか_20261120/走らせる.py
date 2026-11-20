import sys, json, numpy as np
sys.path.insert(0, '../S154_養育者がいないと頼るか_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 参照, 正直 = job; o = 一生(s, 参照, 'v4', 物知り=(1, 正直)); return (s, 参照, 正直) + 数える(o, 6000, 8000) + (o['sha256'],)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(33200, 33230) if 段 == '本' else range(33300, 33330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 参照, 正直) for 参照 in ['養育者', 'ずらし'] for 正直 in [1.0, 0.7, 0.5] for s in S], chunksize=1)
    d = {(s, 参照, 正直): v for s, 参照, 正直, *v in r}; assert len(d) == 180
    res = {'H1_0.7物知り_ずらし>養育者': sum(d[(s, 'ずらし', 0.7)][1] > d[(s, '養育者', 0.7)][1] for s in S),
           'H2_ずらしで0.7>0.5': sum(d[(s, 'ずらし', 0.7)][1] > d[(s, 'ずらし', 0.5)][1] for s in S),
           'sha違う_0.7': sum(d[(s, 'ずらし', 0.7)][4] != d[(s, '養育者', 0.7)][4] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_0.7物知り_ずらし>養育者', 'H2_ずらしで0.7>0.5']}
    res['中央値'] = {f'{参照}_{正直}': [round(float(np.median([d[(s, 参照, 正直)][j] for s in S])), 3) for j in range(4)] for 参照 in ['養育者', 'ずらし'] for 正直 in [1.0, 0.7, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
