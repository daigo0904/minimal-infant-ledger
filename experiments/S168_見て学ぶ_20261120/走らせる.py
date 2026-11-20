import sys, json, numpy as np
sys.path.insert(0, '../S168_見て学ぶ_20261120')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, k = job; o = 一生(s, '見る', 'v4', 種類=(4000,), k代理=k)
    return (s, k) + tuple(種類の差(o, s, 4000, lo, hi) for lo, hi in [(3000, 4000), (4000, 4300), (4000, 4600), (7000, 8000)]) + (float(o['食列'][4000:5000].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(35400, 35430) if 段 == '本' else range(35500, 35530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [0.0, 3.0] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_見て学ぶと早い': sum(d[(s, 3.0)][2] > d[(s, 0.0)][2] for s in S), 'H2_会い始めから見分ける': sum(d[(s, 3.0)][1] > 0 for s in S), 'H3_食べで損をしない': sum(d[(s, 3.0)][4] >= d[(s, 0.0)][4] for s in S),
           'sha違う': sum(d[(s, 3.0)][5] != d[(s, 0.0)][5] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_見て学ぶと早い', 'H2_会い始めから見分ける', 'H3_食べで損をしない']}
    res['中央値'] = {f'代理{k}': dict(zip(['前半の終わり', '4000-4300', '4000-4600', '7000-8000', '食べ4000-5000'], [round(float(np.median([d[(s, k)][j] for s in S])), 4) for j in range(5)])) for k in [0.0, 3.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
