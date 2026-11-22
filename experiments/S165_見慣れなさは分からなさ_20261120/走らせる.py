import sys, json, numpy as np
sys.path.insert(0, '../S165_見慣れなさは分からなさ_20261120')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, k = job; o = 一生(s, '見る', 'v4', 知らない=(4000, 0.3), kU=k); x = 人見(o, 4000, 5000); y = 人見(o, 7000, 8000)
    return (s, k, (x[0] + x[2]) / 2 - (x[4] + x[6]) / 2, (x[1] + x[3]) / 2 - (x[5] + x[7]) / 2, (y[0] + y[2]) / 2 - (y[4] + y[6]) / 2, (y[1] + y[3]) / 2 - (y[5] + y[7]) / 2, 数える(o, 7000, 8000)[0], float(o['食列'][6000:].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(35000, 35030) if 段 == '本' else range(35100, 35130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [0.0, 0.2] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_控える': sum(d[(s, 0.2)][0] < 0 for s in S), 'H2_顔を見る': sum(d[(s, 0.2)][1] > 0 for s in S), 'H3_慣れる': sum(d[(s, 0.2)][0] < d[(s, 0.2)][2] for s in S),
           'H4_kUのおかげ': sum(d[(s, 0.2)][0] < d[(s, 0.0)][0] for s in S), 'H5_情報探しを保つ': sum(d[(s, 0.2)][4] > 0 for s in S), 'sha違う': sum(d[(s, 0.2)][6] != d[(s, 0.0)][6] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_控える', 'H2_顔を見る', 'H3_慣れる', 'H4_kUのおかげ', 'H5_情報探しを保つ']}
    res['中央値'] = {f'kU{k}': dict(zip(['会い始め取る差', '会い始め見る差', '慣れた後取る差', '慣れた後見る差', '情報探し', '食べ'], [round(float(np.median([d[(s, k)][j] for s in S])), 4) for j in range(6)])) for k in [0.0, 0.2]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
