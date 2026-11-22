import sys, json, numpy as np
sys.path.insert(0, '../S225_公平_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, v = job; return (s, v) + tuple(数え.測る(s, v))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(46600, 46630) if 段 == '本' else range(46700, 46730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, v) for v in [True, False] for s in S], chunksize=1)
    d = {(s, v): x for s, v, *x in r}; assert len(d) == 60; v = lambda s, a, k: d[(s, a)][k]
    res = {'H1_少ない子を選ぶ': int(sum(v(s, True, 0) > 0 for s in S)), 'H2_入力のおかげ': int(sum(v(s, True, 0) > v(s, False, 0) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['参考_入力なしで多い子を選ぶ（<0）'] = int(sum(v(s, False, 0) < 0 for s in S))
    res['中央値'] = {('入力あり' if a else '入力なし'): dict(少ない多い差=round(float(np.median([v(s, a, 0) for s in S])), 4), 空腹差=round(float(np.median([v(s, a, 1) for s in S])), 4), なぐさめ=round(float(np.median([v(s, a, 2) for s in S])), 3)) for a in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
