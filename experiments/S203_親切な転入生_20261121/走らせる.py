import sys, json, numpy as np
sys.path.insert(0, '../S203_親切な転入生_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(42200, 42230) if 段 == '本' else range(42300, 42330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [1.0, 3.0] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_よくなぐさめる': int(sum(d[(s, 3.0)][6] > d[(s, 1.0)][6] for s in S)), 'H2_すぐなじむ': int(sum(d[(s, 3.0)][3] > d[(s, 1.0)][3] for s in S)),
           'H3_やがて輪に入る': int(sum(d[(s, 3.0)][5] > d[(s, 1.0)][5] for s in S)), 'H4_やがて助けてもらえる': int(sum(d[(s, 3.0)][2] > d[(s, 1.0)][2] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'親切{k}': dict(zip(['受0', '受1', '受2', '入0', '入1', '入2', '手3'], [round(float(np.median([d[(s, k)][j] for s in S])), 3) for j in range(7)])) for k in [1.0, 3.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
