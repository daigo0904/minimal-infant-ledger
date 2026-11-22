import sys, json, numpy as np
sys.path.insert(0, '../S219_嘘つきの噂_20261121')
from multiprocessing import Pool
腕 = {'噂・嘘つきなし': (0.05, False), '噂・嘘つき1人': (0.05, True), '噂なし': (0.0, False)}
def one(job):
    import 数え; s, 名 = job; g, u = 腕[名]; return (s, 名) + 数え.測る(s, 噂=g, 嘘=u)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(45400, 45430) if 段 == '本' else range(45500, 45530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 90; g = lambda s, 名: d[(s, 名)][0]; c = lambda s, 名: d[(s, 名)][1]
    res = {'H1_嘘つきで得が減る': int(sum(g(s, '噂・嘘つき1人') < g(s, '噂・嘘つきなし') for s in S)), 'H2_嘘つきで表が狂う': int(sum(c(s, '噂・嘘つき1人') < c(s, '噂・嘘つきなし') for s in S)), 'H3_噂なしより得が小': int(sum(g(s, '噂・嘘つき1人') < g(s, '噂なし') for s in S)), 'H4_嘘つきがいても親切は得': int(sum(g(s, '噂・嘘つき1人') > 0 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(得=round(float(np.median([g(s, 名) for s in S])), 4), 表の相関=round(float(np.median([c(s, 名) for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
