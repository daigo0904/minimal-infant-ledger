import sys, json, numpy as np
sys.path.insert(0, '../S238_得がぶつかる世界_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(49200, 49230) if 段 == '本' else range(49300, 49330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [True, False] for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 60; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_競うと当たらない': int(sum(v(s, True, 0) < v(s, False, 0) for s in S)), 'H2_だまされる（偶然より下）': int(sum(v(s, True, 0) < 0.25 for s in S)), 'H3_話し手の言い方も弱まる': int(sum(v(s, True, 2) < v(s, False, 2) for s in S)), 'H4_言葉が崩れる（全体）': int(sum(v(s, True, 1) < v(s, False, 1) for s in S)), 'H5_ほぼ偶然': int(sum(abs(v(s, True, 0) - 0.25) < 0.02 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {('競う' if k else '協力'): dict(当たり=round(float(np.median([v(s, k, 0) for s in S])), 3), 全体=round(float(np.median([v(s, k, 1) for s in S])), 3), 話し手ごと=round(float(np.median([v(s, k, 2) for s in S])), 3)) for k in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
