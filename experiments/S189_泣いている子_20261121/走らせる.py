import sys, json, numpy as np
sys.path.insert(0, '../S189_泣いている子_20261121')
from multiprocessing import Pool
from 共 import *
腕 = {'泣き_kE0': (0.0, 0.01), '泣き_kE50': (50.0, 0.01), 'なし_kE50': (50.0, 0.0)}
def one(job): s, 名 = job; k, x = 腕[名]; o = 一生(s, 'v4', なぐさめ=True, kE=k, 共感型='苦しさ', 泣き=x); return (s, 名) + 泣きなぐさめ(o, 7000, 8000) + (float(o['食列'][7000:].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(39400, 39430) if 段 == '本' else range(39500, 39530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    g = lambda s, 名: d[(s, 名)][0] if d[(s, 名)][0] == d[(s, 名)][0] else -9.0   # 泣いている手が無い世界は 差 を負とみなす
    res = {'H1_泣いている子を選ぶ': sum(g(s, '泣き_kE50') > 0 for s in S), 'H2_共感のおかげ': sum(g(s, '泣き_kE50') > g(s, '泣き_kE0') for s in S), 'H3_泣きのおかげ': sum(g(s, '泣き_kE50') > g(s, 'なし_kE50') for s in S), 'H4_共感なしでも選ぶ': sum(g(s, '泣き_kE0') > 0 for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['泣いている−いない', '泣いている時', 'いない時', '相手>0.5の割合', '90%点', '中央値', '食べ'], [round(float(np.nanmedian([d[(s, 名)][j] for s in S])), 4) for j in range(7)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
