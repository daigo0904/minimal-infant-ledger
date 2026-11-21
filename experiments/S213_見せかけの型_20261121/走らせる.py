import sys, json, numpy as np
sys.path.insert(0, '../S213_見せかけの型_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, v = job; return (s, v) + 数え.測る(s, 見評=v)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(44200, 44230) if 段 == '本' else range(44300, 44330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, v) for v in [True, False] for s in S], chunksize=1)
    d = {(s, v): x for s, v, *x in r}; assert len(d) == 60; 差 = lambda s, v: d[(s, v)][1] - d[(s, v)][0]
    res = {'H1_見せかけが勝つ': int(sum(差(s, True) > 0 for s in S)), 'H2_見られ評判のおかげ': int(sum(差(s, True) > 差(s, False) for s in S)), 'H3_いつも親切が勝つ': int(sum(差(s, True) < 0 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {('見られ評判' if v else 'いつも評判'): dict(いつも=round(float(np.median([d[(s, v)][0] for s in S])), 2), 見せ=round(float(np.median([d[(s, v)][1] for s in S])), 2), 差=round(float(np.median([差(s, v) for s in S])), 2), いつも0=int(sum(d[(s, v)][0] == 0 for s in S)), 見せ0=int(sum(d[(s, v)][1] == 0 for s in S))) for v in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
