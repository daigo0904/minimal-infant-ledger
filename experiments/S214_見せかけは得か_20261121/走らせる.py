import sys, json, numpy as np
sys.path.insert(0, '../S214_見せかけは得か_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, v = job; return (s, v) + 数え.測る(s, 見評=v)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(44400, 44430) if 段 == '本' else range(44500, 44530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, v) for v in [True, False] for s in S], chunksize=1)
    d = {(s, v): x for s, v, *x in r}; assert len(d) == 60
    res = {'H1_見せかけが得': int(sum(d[(s, True)][0] < 0 for s in S)), 'H2_見られ評判のおかげ': int(sum(d[(s, True)][0] < d[(s, False)][0] for s in S)), 'H3_いつも親切は親切でないより得': int(sum(d[(s, True)][2] < d[(s, True)][3] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {('見られ評判' if v else 'いつも評判'): dict(差=round(float(np.median([d[(s, v)][0] for s in S])), 4), 見せ=round(float(np.median([d[(s, v)][1] for s in S])), 4), いつも=round(float(np.median([d[(s, v)][2] for s in S])), 4), 親切でない=round(float(np.median([d[(s, v)][3] for s in S])), 4)) for v in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
