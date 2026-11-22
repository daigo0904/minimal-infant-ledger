import sys, json, numpy as np
sys.path.insert(0, '../S191_お返し_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(39800, 39830) if 段 == '本' else range(39900, 39930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [0.0, 50.0] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_共感でお返し': sum(d[(s, 50.0)][0] > 0 for s in S), 'H2_共感なしでもお返し': sum(d[(s, 0.0)][0] > 0 for s in S), 'H3_はっきりしたお返し': sum(d[(s, 50.0)][0] > 0.02 for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kE{k}': dict(zip(['恩あり−なし', '恩あり', '恩なし', '恩ありの手数'], [round(float(np.median([d[(s, k)][j] for s in S])), 4) for j in range(4)])) for k in [0.0, 50.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
