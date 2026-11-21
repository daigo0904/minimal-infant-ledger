import sys, json, numpy as np
sys.path.insert(0, '../S231_方言_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, m = job; return (s, m) + tuple(数え.測る(s, m))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(47800, 47830) if 段 == '本' else range(47900, 47930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, m) for m in [0.02, 0.5] for s in S], chunksize=1)
    d = {(s, m): x for s, m, *x in r}; assert len(d) == 60; v = lambda s, m, j: d[(s, m)][j]
    res = {'H1_群れごとに別の言葉': int(sum(v(s, 0.02, 1) < v(s, 0.02, 0) for s in S)), 'H2_混ざらないせい': int(sum(v(s, 0.02, 1) < v(s, 0.5, 1) for s in S)), 'H3_よその群れとは通じない': int(sum(v(s, 0.02, 3) < v(s, 0.02, 2) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['参考_m0.02で群れどうし完全一致の世界'] = int(sum(v(s, 0.02, 1) == 1.0 for s in S))
    res['中央値'] = {f'm{m}': dict(群れの中の一致=round(float(np.median([v(s, m, 0) for s in S])), 3), 群れどうしの一致=round(float(np.median([v(s, m, 1) for s in S])), 3), 当たり中=round(float(np.median([v(s, m, 2) for s in S])), 3), 当たりまたぐ=round(float(np.median([v(s, m, 3) for s in S])), 3)) for m in [0.02, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
