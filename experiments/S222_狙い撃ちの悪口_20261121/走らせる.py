import sys, json, numpy as np
sys.path.insert(0, '../S222_狙い撃ちの悪口_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, 悪 = job; return (s, 悪) + tuple(数え.測る(s, 悪=悪))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(46000, 46030) if 段 == '本' else range(46100, 46130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, v) for v in [True, False] for s in S], chunksize=1)
    d = {(s, v): x for s, v, *x in r}; assert len(d) == 60; v = lambda s, a, k: d[(s, a)][k]
    res = {'H1_標的が損をする': int(sum(v(s, True, 0) > 0 for s in S)), 'H2_悪口のせい': int(sum(v(s, True, 0) > v(s, False, 0) for s in S)), 'H3_見抜けない': int(sum(v(s, True, 1) > 0.5 for s in S)), 'H4_標的の評判が下がる': int(sum(v(s, True, 3) < v(s, False, 3) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {('悪口あり' if a else '悪口なし'): dict(標的の損=round(float(np.median([v(s, a, 0) for s in S])), 4), 嘘つきへの信用=round(float(np.median([v(s, a, 1) for s in S])), 3), 正直への信用=round(float(np.median([v(s, a, 2) for s in S])), 3), 標的の評判差=round(float(np.median([v(s, a, 3) for s in S])), 3)) for a in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
