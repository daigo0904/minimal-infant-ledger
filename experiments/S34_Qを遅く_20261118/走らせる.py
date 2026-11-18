import sys, json, numpy as np
from multiprocessing import Pool
import 頭 as H
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(10200, 10210) if 段 == '本' else range(10300, 10310)
    with Pool(8) as p: r = p.map(H.one, [(s, lr) for lr in [0.05, 0.01] for s in S])
    d = {(s, lr): (f, g, h) for s, lr, f, g, h in r}
    res = dict(H1_漏れが減る=int(sum(d[(s, 0.01)][1][1] < d[(s, 0.05)][1][1] for s in S)), H2_育ちで出る=int(sum(d[(s, 0.01)][0][2] <= d[(s, 0.01)][1][2] / 2 for s in S)),
               H3_飢えない=int(sum(d[(s, 0.01)][2] <= d[(s, 0.05)][2] for s in S)))
    res['判定'] = {k: v >= 8 for k, v in res.items()}
    res['中央値'] = {str(lr): dict(初め差=round(float(np.median([d[(s, lr)][0][2] for s in S])), 3), 育_P養P他差=[round(float(np.median([d[(s, lr)][1][j] for s in S])), 3) for j in range(3)], 空腹=round(float(np.median([d[(s, lr)][2] for s in S])), 3)) for lr in [0.05, 0.01]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
