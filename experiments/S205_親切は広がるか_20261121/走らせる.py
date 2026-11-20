import sys, json, numpy as np
sys.path.insert(0, '../S205_親切は広がるか_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(42600, 42630) if 段 == '本' else range(42700, 42730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [1.0, 0.0] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_恩が返らないと減る': int(sum(d[(s, 0.0)][0] < 4 for s in S)), 'H2_恩が返ると残る': int(sum(d[(s, 1.0)][0] > d[(s, 0.0)][0] for s in S)), 'H3_恩が返ると広がる': int(sum(d[(s, 1.0)][0] > 4 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kG{k}': round(float(np.median([d[(s, k)][0] for s in S])), 2) for k in [1.0, 0.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
