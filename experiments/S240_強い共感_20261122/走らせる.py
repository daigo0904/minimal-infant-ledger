import sys, json, numpy as np
sys.path.insert(0, '../S240_強い共感_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(49600, 49630) if 段 == '本' else range(49700, 49730)); K = [0.0, 50.0, 500.0]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in K for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 90; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_強い共感で当たる': int(sum(v(s, 500.0, 0) > v(s, 50.0, 0) for s in S)), 'H2_強い共感で言葉が戻る': int(sum(v(s, 500.0, 0) > 0.30 for s in S)), 'H3_共感があると当たる': int(sum(v(s, 50.0, 0) > v(s, 0.0, 0) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {f'kE{k}': dict(当たり=round(float(np.median([v(s, k, 0) for s in S])), 3), 全体=round(float(np.median([v(s, k, 1) for s in S])), 3), 話し手ごと=round(float(np.median([v(s, k, 2) for s in S])), 3)) for k in K}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
