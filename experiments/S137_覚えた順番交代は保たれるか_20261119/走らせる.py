import sys, json, numpy as np
sys.path.insert(0, '../S137_覚えた順番交代は保たれるか_20261119')
from multiprocessing import Pool
from 共 import *
腕 = [None, '褒めだけ', 'でたらめ']
def one(job): s, 後 = job; o = 一生(s, '交代', 番後=後); return (s, str(後)) + 数える(o, 3000, 4000) + 数える(o, 4000, 5000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(30200, 30230) if 段 == '本' else range(30300, 30330)
    with Pool(8) as p: r = p.map(one, [(s, 後) for 後 in 腕 for s in S])
    d = {(s, 後): v for s, 後, *v in r}
    res = {'H1_褒めはでたらめより長く保つ（終わり）': int(sum(d[(s, '褒めだけ')][10] > d[(s, 'でたらめ')][10] for s in S)),
           'H2_褒めだけでは崩れていく（終わり<切替前）': int(sum(d[(s, '褒めだけ')][10] < d[(s, '褒めだけ')][2] for s in S)),
           'H3_褒めだけでも終わりに残る（差>0）': int(sum(d[(s, '褒めだけ')][10] > 0 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {後: dict(切替前の差=round(float(np.median([d[(s, 後)][2] for s in S])), 3), 切替後1000手の差=round(float(np.median([d[(s, 後)][6] for s in S])), 3), 終わりの差=round(float(np.median([d[(s, 後)][10] for s in S])), 3), 終わりの話す時に声=round(float(np.median([d[(s, 後)][9] for s in S])), 3)) for 後 in map(str, 腕)}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
