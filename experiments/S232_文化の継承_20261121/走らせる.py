import sys, json, numpy as np
sys.path.insert(0, '../S232_文化の継承_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(48000, 48030) if 段 == '本' else range(48100, 48130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in ['耳', 'ふつう'] for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 60; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_最初の言葉が最後まで残る': int(sum(v(s, '耳', 0) == 1.0 for s in S)), 'H2_ふつうより残る': int(sum(v(s, '耳', 0) > v(s, 'ふつう', 0) for s in S)), 'H3_入れ替わっても通じる': int(sum(v(s, '耳', 1) > 0.7 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {k: dict(最初の言葉との一致=round(float(np.median([v(s, k, 0) for s in S])), 3), 最後の当たり=round(float(np.median([v(s, k, 1) for s in S])), 3), 最後のそろい=round(float(np.median([v(s, k, 2) for s in S])), 3)) for k in ['耳', 'ふつう']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
