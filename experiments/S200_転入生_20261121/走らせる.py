import sys, json, numpy as np
sys.path.insert(0, '../S200_転入生_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, γ, 転 = job; return (s, γ, 転) + 数え.測る(s, γ, 転入=転)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(41600, 41630) if 段 == '本' else range(41700, 41730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, γ, 転) for γ in [0.0, 5.0] for 転 in [None, 4000] for s in S], chunksize=1)
    d = {(s, γ, 転): v for s, γ, 転, *v in r}; assert len(d) == 120
    res = {'H1_転入生になぐさめが届きにくい_γ0': sum(d[(s, 0.0, 4000)][3] < d[(s, 0.0, None)][3] for s in S), 'H2_同_γ5': sum(d[(s, 5.0, 4000)][3] < d[(s, 5.0, None)][3] for s in S),
           'H3_転入生はお腹が空く_γ0': sum(d[(s, 0.0, 4000)][2] > d[(s, 0.0, None)][2] for s in S), 'H4_困っている子に寄ると転入生が助かる': sum(d[(s, 5.0, 4000)][3] > d[(s, 0.0, 4000)][3] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'γ{γ}_転入{転}': dict(zip(['子0の入り次数', '他の入り次数', '空腹差', 'なぐさめてもらった差'], [round(float(np.median([d[(s, γ, 転)][j] for s in S])), 4) for j in range(4)])) for γ in [0.0, 5.0] for 転 in [None, 4000]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
