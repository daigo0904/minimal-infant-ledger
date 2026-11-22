import sys, json, numpy as np
sys.path.insert(0, '../S185_見られ分けの余韻_20261121')
from multiprocessing import Pool
import 共
def one(job): s, 名 = job; o = 共.一生(s, 名, 記憶=0.5); return (s, 名, [list(共.余韻(o, lo, lo + 1000)) for lo in range(1000, 8000, 1000)])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(39000, 39030) if 段 == '本' else range(39100, 39130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in ['元', 'v4'] for s in S], chunksize=1)
    d = {(s, 名): np.array(v) for s, 名, v in r}; assert len(d) == 60
    res = {'H1_元の余韻は育つ': int(sum(d[(s, '元')][6, 0] > d[(s, '元')][0, 0] for s in S)), 'H2_頭打ちの後も育つ': int(sum(d[(s, '元')][6, 0] > d[(s, '元')][3, 0] for s in S)),
           'H3_見られ分けの後に育つ': int(sum(d[(s, '元')][6, 0] - d[(s, '元')][3, 0] > d[(s, '元')][6, 3] - d[(s, '元')][3, 3] for s in S)), 'H4_v4の余韻は育つ': int(sum(d[(s, 'v4')][6, 0] > d[(s, 'v4')][0, 0] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: {'余韻': [round(float(v), 3) for v in np.median([d[(s, 名)][:, 0] for s in S], 0)], '見られ分け': [round(float(v), 3) for v in np.median([d[(s, 名)][:, 3] for s in S], 0)]} for 名 in ['元', 'v4']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=[(s, 名, v) for s, 名, v in r]), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
