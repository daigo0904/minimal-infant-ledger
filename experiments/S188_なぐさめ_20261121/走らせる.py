import sys, json, numpy as np
sys.path.insert(0, '../S188_なぐさめ_20261121')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, k = job; o = 一生(s, 'v4', なぐさめ=True, kE=k, 共感型='苦しさ'); A, 相 = o['行動列'][7000:], o['相手列'][7000:]
    return (s, k) + なぐさめ方(o, 7000, 8000) + (float((A[相 > 0] == 3).mean()), float(o['食列'][7000:].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(39200, 39230) if 段 == '本' else range(39300, 39330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [0.0, 50.0] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_共感なしでも困った子を': sum(d[(s, 0.0)][0] > 0 for s in S), 'H2_共感でなぐさめが増える': sum(d[(s, 50.0)][4] > d[(s, 0.0)][4] for s in S),
           'H3_共感で相手が楽になる': sum(d[(s, 50.0)][3] < d[(s, 0.0)][3] for s in S), 'H4_共感で困った子を選ぶ': sum(d[(s, 50.0)][0] > 0 for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kE{k}': dict(zip(['困っている−いない', '困っている時', 'いない時', '相手の空腹', '仲間の前の手3', '食べ'], [round(float(np.median([d[(s, k)][j] for s in S])), 4) for j in range(6)])) for k in [0.0, 50.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
