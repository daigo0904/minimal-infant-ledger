import sys, json, numpy as np
sys.path.insert(0, '../S228_二人だけの言葉_20261121')
from multiprocessing import Pool
腕 = ['毎回', '固定', '固定・役交代']
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(47200, 47230) if 段 == '本' else range(47300, 47330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in 腕 for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 90; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_固定で全体の結びつきが大': int(sum(v(s, '固定', 1) > v(s, '毎回', 1) for s in S)), 'H2_固定で当たりが大': int(sum(v(s, '固定', 0) > v(s, '毎回', 0) for s in S)), 'H3_役交代で当たりが大': int(sum(v(s, '固定・役交代', 0) > v(s, '毎回', 0) for s in S)), 'H4_役交代で一人ひとりの言い方がはっきり': int(sum(v(s, '固定・役交代', 2) > v(s, '毎回', 2) for s in S)), 'H5_毎回でも一人ひとりの言い方ははっきり': int(sum(v(s, '毎回', 2) > 0.5 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {k: dict(当たり=round(float(np.median([v(s, k, 0) for s in S])), 3), 全体の結びつき=round(float(np.median([v(s, k, 1) for s in S])), 3), 話し手ごとの結びつき=round(float(np.median([v(s, k, 2) for s in S])), 3)) for k in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
