import sys, json, numpy as np
sys.path.insert(0, '../S178_生まれつきの自分の好み_20261120')
from multiprocessing import Pool
from 共 import 一生, ブロッコリー
def one(job): s, k = job; o = 一生(s, 'v4', 二人=0.5, 自分=0.05, k生まれ=k); return (s, k, [list(ブロッコリー(o, lo, lo + 1000)) for lo in range(0, 8000, 1000)], o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(37000, 37030) if 段 == '本' else range(37100, 37130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [0.1, 0.0] for s in S], chunksize=1)
    d = {(s, k): np.array(v) for s, k, v, h in r}; assert len(d) == 60
    res = {'H1_初めは自分中心': int(sum(d[(s, 0.1)][0, 0] < 0 for s in S)), 'H2_後で相手に合わせる': int(sum(d[(s, 0.1)][7, 0] > 0 for s in S)),
           'H3_切り替わる': int(sum(d[(s, 0.1)][0, 0] < 0 and d[(s, 0.1)][7, 0] > 0 for s in S)), 'H4_生まれつきのせい': int(sum(d[(s, 0.1)][0, 0] < d[(s, 0.0)][0, 0] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'k生まれ{k}': {'B前の差': [round(float(v), 3) for v in np.median([d[(s, k)][:, 0] for s in S], 0)], '仲間前の自分好き': [round(float(v), 3) for v in np.median([d[(s, k)][:, 1] for s in S], 0)]} for k in [0.1, 0.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
