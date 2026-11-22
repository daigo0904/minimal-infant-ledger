import sys, json, numpy as np
sys.path.insert(0, '../S224_頑固さの代価_20261121')
from multiprocessing import Pool
腕 = {'噂なし': (0.0, None), '噂のみ': (0.05, None), '噂＋ふるい': (0.05, 0.05)}
def one(job):
    import 数え; s, 名 = job; g, f = 腕[名]; return (s, 名) + tuple(数え.測る(s, 噂=g, ふるい=f))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(46400, 46430) if 段 == '本' else range(46500, 46530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 90; v = lambda s, 名, k: d[(s, 名)][k]
    F, G, Z = '噂＋ふるい', '噂のみ', '噂なし'
    res = {'H1_ふるいで噂のみより遅い': int(sum(v(s, F, 0) > v(s, G, 0) for s in S)), 'H2_ふるいで噂なしより遅い': int(sum(v(s, F, 0) > v(s, Z, 0) for s in S)), 'H3_ふるいで変わる子が空腹': int(sum(v(s, F, 1) > v(s, G, 1) for s in S)), 'H4_ふるいで噂のみより速い': int(sum(v(s, F, 0) < v(s, G, 0) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {名: dict(追いつく手数=float(np.median([v(s, 名, 0) for s in S])), 変わる子の空腹=round(float(np.median([v(s, 名, 1) for s in S])), 3), 評判の上がり=round(float(np.median([v(s, 名, 2) for s in S])), 3), 届かず=int(sum(v(s, 名, 0) >= 8000 for s in S))) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
