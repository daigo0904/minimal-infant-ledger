import sys, json, numpy as np
sys.path.insert(0, '../S230_言葉の習得_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(47600, 47630) if 段 == '本' else range(47700, 47730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in ['耳', 'ふつう'] for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 60; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_新入りが仲間の言い方で話す': int(sum(v(s, '耳', 2) > 0.5 for s in S)), 'H2_ふつうの世界より': int(sum(v(s, '耳', 2) > v(s, 'ふつう', 2) for s in S)), 'H3_聞き取りが上達する': int(sum(v(s, '耳', 1) > v(s, '耳', 0) for s in S)), 'H4_来てすぐ半分以上わかる': int(sum(v(s, '耳', 0) > 0.5 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {k: dict(来てすぐの当たり=round(float(np.median([v(s, k, 0) for s in S])), 3), 最後の当たり=round(float(np.median([v(s, k, 1) for s in S])), 3), 言い方の一致=round(float(np.median([v(s, k, 2) for s in S])), 3)) for k in ['耳', 'ふつう']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
