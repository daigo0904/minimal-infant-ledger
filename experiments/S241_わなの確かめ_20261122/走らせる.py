import sys, json, numpy as np
sys.path.insert(0, '../S241_わなの確かめ_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(49800, 49830) if 段 == '本' else range(49900, 49930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [500.0, 50.0] for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 60; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_強い共感なら最後も当たる': int(sum(v(s, 500.0, 1) > v(s, 50.0, 1) for s in S)), 'H2_強い共感で言葉が守られる（>0.30）': int(sum(v(s, 500.0, 1) > 0.30 for s in S)), 'H3_kE50は競うと下がる': int(sum(v(s, 50.0, 1) < v(s, 50.0, 0) for s in S)), 'H4_合図と場所の結びつきは残る（>0.1）': int(sum(v(s, 50.0, 3) > 0.1 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {f'kE{k}': dict(当たり前=round(float(np.median([v(s, k, 0) for s in S])), 3), 当たり最後=round(float(np.median([v(s, k, 1) for s in S])), 3), 結びつき前=round(float(np.median([v(s, k, 2) for s in S])), 3), 結びつき最後=round(float(np.median([v(s, k, 3) for s in S])), 3)) for k in [500.0, 50.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
