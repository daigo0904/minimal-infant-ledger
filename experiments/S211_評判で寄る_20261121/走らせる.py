import sys, json, numpy as np
sys.path.insert(0, '../S211_評判で寄る_20261121')
from multiprocessing import Pool
腕 = {'β0ρ5_親切': (0.0, 3.0, 5.0), 'β0ρ5_対照': (0.0, 1.0, 5.0), 'β0ρ0_親切': (0.0, 3.0, 0.0), 'β.3ρ5_親切': (0.3, 3.0, 5.0), 'β.3ρ5_対照': (0.3, 1.0, 5.0)}
def one(job):
    import 数え; s, 名 = job; β, k, ρ = 腕[名]; return (s, 名) + 数え.測る(s, 1.0, β=β, 親切=k, ρ=ρ)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(43800, 43830) if 段 == '本' else range(43900, 43930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 150
    勝 = lambda a, b: int(sum(d[(s, a)][0] > d[(s, b)][0] for s in S))
    res = {'H1_評判で親切が有利': 勝('β0ρ5_親切', 'β0ρ5_対照'), 'H2_評判のおかげ': 勝('β0ρ5_親切', 'β0ρ0_親切'), 'H3_広がる': int(sum(d[(s, 'β0ρ5_親切')][0] > 4 for s in S)), 'H4_恩人に寄る世界でも有利': 勝('β.3ρ5_親切', 'β.3ρ5_対照')}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(終わり=round(float(np.median([d[(s, 名)][0] for s in S])), 2), 終わり0の世界=int(sum(d[(s, 名)][0] == 0 for s in S))) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
