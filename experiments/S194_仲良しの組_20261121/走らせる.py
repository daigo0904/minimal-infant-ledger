import sys, json, numpy as np
sys.path.insert(0, '../S194_仲良しの組_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(40200, 40230) if 段 == '本' else range(40300, 40330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [0.0, 1.0] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_助け合う組ができる': sum(d[(s, 1.0)][0] > 0 for s in S), 'H2_感謝のおかげ': sum(d[(s, 1.0)][0] > d[(s, 0.0)][0] for s in S), 'H3_親友ができる': sum(d[(s, 1.0)][1] > d[(s, 0.0)][1] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kG{k}': dict(zip(['相関', '偏り'], [round(float(np.median([d[(s, k)][j] for s in S])), 4) for j in range(2)])) for k in [0.0, 1.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
