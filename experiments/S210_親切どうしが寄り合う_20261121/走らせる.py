import sys, json, numpy as np
sys.path.insert(0, '../S210_親切どうしが寄り合う_20261121')
from multiprocessing import Pool
腕 = {'δ2_親切': (3.0, 2.0), 'δ2_対照': (1.0, 2.0), 'δ0_親切': (3.0, 0.0)}
def one(job):
    import 数え; s, 名 = job; k, δ = 腕[名]; return (s, 名) + 数え.測る(s, 1.0, β=0.3, 親切=k, δ=δ)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(43600, 43630) if 段 == '本' else range(43700, 43730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_寄り合えば有利': int(sum(d[(s, 'δ2_親切')][0] > d[(s, 'δ2_対照')][0] for s in S)), 'H2_寄り合いのおかげ': int(sum(d[(s, 'δ2_親切')][0] > d[(s, 'δ0_親切')][0] for s in S)), 'H3_広がる': int(sum(d[(s, 'δ2_親切')][0] > 4 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(終わり=round(float(np.median([d[(s, 名)][0] for s in S])), 2), 終わり0の世界=int(sum(d[(s, 名)][0] == 0 for s in S))) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
