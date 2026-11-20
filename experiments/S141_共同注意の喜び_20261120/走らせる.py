import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S141選び', '../S141_共同注意の喜び_20261120/選び.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
腕 = {'全部 kJ0': dict(kf=3.0, kD=30.0, λ=0.2), '全部 kJ3': dict(kf=3.0, kD=30.0, λ=0.2, kJ=3.0)}
def one(job): s, 名 = job; return (s, 名) + tuple(G.one((s, 腕[名])))
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(31200, 31230) if 段 == '本' else range(31300, 31330)
    with Pool(8) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S])
    d = {(s, 名): v for s, 名, *v in r}
    res = {'H1_共同注意の喜びで叙述的指さしが育つ': int(sum(d[(s, '全部 kJ3')][0] > 0 for s in S)), 'H2_喜びなしより育つ': int(sum(d[(s, '全部 kJ3')][0] > d[(s, '全部 kJ0')][0] for s in S)),
           'H3_代わりに食べ物が減る': int(sum(d[(s, '全部 kJ3')][2] < d[(s, '全部 kJ0')][2] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(育ち=round(float(np.median([d[(s, 名)][0] for s in S])), 3), 終わりの指す=round(float(np.median([d[(s, 名)][1] for s in S])), 3), 食べ=round(float(np.median([d[(s, 名)][2] for s in S])), 4)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
