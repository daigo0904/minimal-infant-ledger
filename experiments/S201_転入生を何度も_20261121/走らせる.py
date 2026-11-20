import sys, json, numpy as np
sys.path.insert(0, '../S201_転入生を何度も_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(41800, 41830) if 段 == '本' else range(41900, 41930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, γ) for γ in [0.0, 5.0] for s in S], chunksize=1)
    d = {(s, γ): v for s, γ, *v in r}; assert len(d) == 60
    res = {'H1_転入生になぐさめが届かない': sum(d[(s, 0.0)][0] < 0 for s in S), 'H2_一番に選ばれにくい': sum(d[(s, 0.0)][1] < 0 for s in S), 'H3_γ5でも届かない': sum(d[(s, 5.0)][0] < 0 for s in S), 'H4_γ5で助かる': sum(d[(s, 5.0)][0] > d[(s, 0.0)][0] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'γ{γ}': dict(zip(['なぐさめてもらった差', '入り次数の差'], [round(float(np.median([d[(s, γ)][j] for s in S])), 3) for j in range(2)])) for γ in [0.0, 5.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
