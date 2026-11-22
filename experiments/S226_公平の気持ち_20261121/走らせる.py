import sys, json, numpy as np
sys.path.insert(0, '../S226_公平の気持ち_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(46800, 46830) if 段 == '本' else range(46900, 46930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [5.0, 0.0] for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 60; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_少ない子を選ぶ': int(sum(v(s, 5.0, 0) > 0 for s in S)), 'H2_公平の気持ちのおかげ': int(sum(v(s, 5.0, 0) > v(s, 0.0, 0) for s in S)), 'H3_なぐさめの偏りが減る': int(sum(v(s, 5.0, 1) < v(s, 0.0, 1) for s in S)), 'H4_空腹のばらつきが減る': int(sum(v(s, 5.0, 2) < v(s, 0.0, 2) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {f'kQ{k}': dict(少ない多い差=round(float(np.median([v(s, k, 0) for s in S])), 4), 変動係数=round(float(np.median([v(s, k, 1) for s in S])), 3), 空腹のばらつき=round(float(np.median([v(s, k, 2) for s in S])), 4), なぐさめ=round(float(np.median([v(s, k, 3) for s in S])), 3)) for k in [5.0, 0.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
