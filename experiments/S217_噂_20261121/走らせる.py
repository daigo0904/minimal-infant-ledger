import sys, json, numpy as np
sys.path.insert(0, '../S217_噂_20261121')
from multiprocessing import Pool
腕 = {'見た・噂なし': (5.0, '見た', 0.0), '見た・噂0.01': (5.0, '見た', 0.01), '見た・噂0.05': (5.0, '見た', 0.05), '共有': (5.0, False, 0.0)}
def one(job):
    import 数え; s, 名 = job; ρ, 私, g = 腕[名]; return (s, 名) + 数え.測る(s, ρ=ρ, 私的=私, 噂=g)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(45000, 45030) if 段 == '本' else range(45100, 45130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 120; g = lambda s, 名: d[(s, 名)][0]; c = lambda s, 名: d[(s, 名)][1]
    res = {'H1_噂で得が増える': int(sum(g(s, '見た・噂0.01') > g(s, '見た・噂なし') for s in S)), 'H2_噂で共有に近づく': int(sum(abs(g(s, '共有') - g(s, '見た・噂0.01')) < abs(g(s, '共有') - g(s, '見た・噂なし')) for s in S)), 'H3_噂で表が正しくなる': int(sum(c(s, '見た・噂0.01') > c(s, '見た・噂なし') for s in S)), 'H4_強い噂で得が減る': int(sum(g(s, '見た・噂0.05') < g(s, '見た・噂なし') for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(得=round(float(np.median([g(s, 名) for s in S])), 4), 表の相関=(round(float(np.median([c(s, 名) for s in S])), 3) if 名 != '共有' else None)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
