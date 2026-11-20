import sys, json, numpy as np
sys.path.insert(0, '../S177_14か月から18か月_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): s, x = job; r, h = 測る(s, 'v4', x); return (s, x, [list(v) for v in r], h)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(36800, 36830) if 段 == '本' else range(36900, 36930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, x) for x in [0.05, 0.1] for s in S], chunksize=1)
    d = {(s, x): np.array(v) for s, x, v, h in r}; assert len(d) == 60
    def 数(x): return {'H1_初めは自分中心': sum(d[(s, x)][0, 0] < 0 for s in S), 'H2_育つ': sum(d[(s, x)][7, 0] > d[(s, x)][0, 0] for s in S), 'H3_切り替わる': sum(d[(s, x)][0, 0] < 0 and d[(s, x)][7, 0] > 0 for s in S)}
    res = 数(0.05); res['判定'] = {k: int(v) >= 20 for k, v in res.items()}; res['参考_自分0.1'] = 数(0.1)
    res = json.loads(json.dumps(res, default=int))
    res['中央値'] = {f'自分{x}': {'B前の差': [round(float(v), 3) for v in np.median([d[(s, x)][:, 0] for s in S], 0)], '仲間前の自分好き': [round(float(v), 3) for v in np.median([d[(s, x)][:, 1] for s in S], 0)]} for x in [0.05, 0.1]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1, default=int)
