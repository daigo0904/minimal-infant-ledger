import sys, json, numpy as np
sys.path.insert(0, '../S244_決まりなしの言葉の習得_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何 = job
    if 何 == '転入': x = (数え.転入(s)[0], 0.0)
    elif 何 == '群れ': x = tuple(数え.群れ(s)[:2])
    else: x = tuple(数え.継承(s)[:2])
    return (s, 何) + x
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(50400, 50430) if 段 == '本' else range(50500, 50530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 何) for 何 in ['転入', '群れ', '継承'] for s in S], chunksize=1)
    d = {(s, 何): x for s, 何, *x in r}; assert len(d) == 90
    res = {'H1_新入りが覚える': int(sum(d[(s, '転入')][0] > 0.5 for s in S)), 'H2_方言ができる': int(sum(d[(s, '群れ')][1] < d[(s, '群れ')][0] for s in S)), 'H3_最初の言葉がそのまま残る（1.0）': int(sum(d[(s, '継承')][0] == 1.0 for s in S)), 'H4_入れ替わっても通じる（>0.7）': int(sum(d[(s, '継承')][1] > 0.7 for s in S)), 'H5_言葉が変わる（<1.0）': int(sum(d[(s, '継承')][0] < 1.0 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = dict(新入りの一致=float(np.median([d[(s, '転入')][0] for s in S])), 群れの中=round(float(np.median([d[(s, '群れ')][0] for s in S])), 3), 群れどうし=round(float(np.median([d[(s, '群れ')][1] for s in S])), 3), 最初の言葉との一致=float(np.median([d[(s, '継承')][0] for s in S])), 最後の当たり=round(float(np.median([d[(s, '継承')][1] for s in S])), 3))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
