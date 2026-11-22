import sys, json, numpy as np
sys.path.insert(0, '../S190_なぐさめの代価_20261121')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, x = job; o = 一生(s, 'v4', なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=x); A, 相 = o['行動列'][7000:], o['相手列'][7000:]
    return (s, x) + 泣きなぐさめ(o, 7000, 8000) + (float((A[相 > 0] == 3).mean()), float(o['食列'][7000:].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(39600, 39630) if 段 == '本' else range(39700, 39730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, x) for x in [0.0, 0.03] for s in S], chunksize=1)
    d = {(s, x): v for s, x, *v in r}; assert len(d) == 60
    比 = lambda s, x: d[(s, x)][1] / max(d[(s, x)][2], 1e-9)
    res = {'H1_代価でなぐさめが減る': sum(d[(s, 0.03)][6] < d[(s, 0.0)][6] for s in S), 'H2_代価があっても選ぶ': sum(d[(s, 0.03)][0] > 0 for s in S),
           'H3_泣いている子に絞る_割合': sum(比(s, 0.03) > 比(s, 0.0) for s in S), 'H4_差も大きくなる': sum(d[(s, 0.03)][0] > d[(s, 0.0)][0] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'代価{x}': dict(zip(['泣いている−いない', '泣いている時', 'いない時', '相手>0.5', '90%点', '中央値', '仲間の前の手3', '食べ'], [round(float(np.nanmedian([d[(s, x)][j] for s in S])), 4) for j in range(8)]), 比=round(float(np.median([比(s, x) for s in S])), 3)) for x in [0.0, 0.03]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
