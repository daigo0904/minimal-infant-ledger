import sys, json, numpy as np
from multiprocessing import Pool
import 頭 as H
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(10000, 10010) if 段 == '本' else range(10100, 10110)
    with Pool(8) as p: r = p.map(H.one, [(s, k) for k in [False, True] for s in S])
    d = {(s, k): g for s, k, f, g in r}
    res = dict(H1_漏れが減る=int(sum(d[(s, True)][1] < d[(s, False)][1] for s in S)), H2_見られ分けは負けない=int(sum(d[(s, True)][2] >= d[(s, False)][2] for s in S)))
    res['判定'] = {k: v >= 8 for k, v in res.items()}
    res['中央値_育_P養P他差'] = {('あり' if k else 'なし'): [round(float(np.median([d[(s, k)][j] for s in S])), 3) for j in range(3)] for k in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
