import sys, json, numpy as np
sys.path.insert(0, '../S239_評判で正直を守る_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, ρ = job; return (s, ρ) + tuple(数え.測る(s, ρ))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(49400, 49430) if 段 == '本' else range(49500, 49530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, ρ) for ρ in [5.0, 0.0] for s in S], chunksize=1)
    d = {(s, ρ): x for s, ρ, *x in r}; assert len(d) == 60; v = lambda s, ρ, j: d[(s, ρ)][j]
    res = {'H1_評判で当たりが上がる': int(sum(v(s, 5.0, 0) > v(s, 0.0, 0) for s in S)), 'H2_言葉が戻る（>0.30）': int(sum(v(s, 5.0, 0) > 0.30 for s in S)), 'H3_全体の結びつきが戻る': int(sum(v(s, 5.0, 1) > v(s, 0.0, 1) for s in S)), 'H4_話し手の言い方は弱まる': int(sum(v(s, 5.0, 2) < v(s, 0.0, 2) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {f'ρ{ρ}': dict(当たり=round(float(np.median([v(s, ρ, 0) for s in S])), 3), 全体=round(float(np.median([v(s, ρ, 1) for s in S])), 3), 話し手ごと=round(float(np.median([v(s, ρ, 2) for s in S])), 3)) for ρ in [5.0, 0.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
