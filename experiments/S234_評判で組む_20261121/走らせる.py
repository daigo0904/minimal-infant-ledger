import sys, json, numpy as np
sys.path.insert(0, '../S234_評判で組む_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何, ρ = job; x = (数え.増える(s, ρ)[0], 0.0) if 何 == '増' else tuple(数え.得(s, ρ)[:2]); return (s, 何, ρ) + x
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(48400, 48430) if 段 == '本' else range(48500, 48530))
    J = [(s, 何, ρ) for 何 in ['増', '得'] for ρ in [5.0, 0.0] for s in S]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, J, chunksize=1)
    d = {(s, 何, ρ): x for s, 何, ρ, *x in r}; assert len(d) == 120
    res = {'H1_評判で耳の子が増える': int(sum(d[(s, '増', 5.0)][0] > 4 for s in S)), 'H2_毎回より多い': int(sum(d[(s, '増', 5.0)][0] > d[(s, '増', 0.0)][0] for s in S)), 'H3_耳の子が得': int(sum(d[(s, '得', 5.0)][0] > 0 for s in S)), 'H4_耳どうしが組む': int(sum(d[(s, '得', 5.0)][1] > d[(s, '得', 0.0)][1] for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {f'ρ{ρ}': dict(終わりの耳の子=float(np.median([d[(s, '増', ρ)][0] for s in S])), 空腹差_ふつう引く耳=round(float(np.median([d[(s, '得', ρ)][0] for s in S])), 4), 耳どうしの組=round(float(np.median([d[(s, '得', ρ)][1] for s in S])), 3)) for ρ in [5.0, 0.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
