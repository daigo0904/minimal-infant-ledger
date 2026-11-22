import sys, json, numpy as np
sys.path.insert(0, '../S215_私的な評判_20261121')
from multiprocessing import Pool
腕 = {'共有評判': (5.0, False), '私的評判': (5.0, True), '評判なし': (0.0, False)}
def one(job):
    import 数え; s, 名 = job; ρ, 私 = 腕[名]; return (s, 名) + 数え.測る(s, ρ=ρ, 私的=私)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(44600, 44630) if 段 == '本' else range(44700, 44730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 90; g = lambda s, 名: d[(s, 名)][0]
    res = {'H1_私的評判でも親切が得': int(sum(g(s, '私的評判') > 0 for s in S)), 'H2_評判なしより得': int(sum(g(s, '私的評判') > g(s, '評判なし') for s in S)), 'H3_共有評判より得が小': int(sum(g(s, '私的評判') < g(s, '共有評判') for s in S)), 'H4_共有評判より得が大': int(sum(g(s, '私的評判') > g(s, '共有評判') for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(得=round(float(np.median([d[(s, 名)][0] for s in S])), 4), 親切=round(float(np.median([d[(s, 名)][1] for s in S])), 3), 親切でない=round(float(np.median([d[(s, 名)][2] for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
