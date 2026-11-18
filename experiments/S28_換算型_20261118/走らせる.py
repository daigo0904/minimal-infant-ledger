import json, sys, numpy as np
from multiprocessing import Pool
import 頭 as H
H.c[0] = 30.0
def one(job):
    s, a = job; H.c[0] = 30.0
    o = H.一生(s, '道具型') if a == '道具' else H.一生(s, '獲得型', 換算する=(a == '換算'))
    return (s, a) + H.数字(o)
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(9000, 9010) if 段 == '本' else range(9100, 9110)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['道具', '元', '換算'] for s in S])
    d = {(s, a): (f, g) for s, a, f, g in r}
    差 = lambda s, a, k: d[(s, a)][k] - d[(s, '道具')][k]
    res = dict(H1_差が育つ=int(sum(差(s, '換算', 1) > 差(s, '換算', 0) for s in S)), H2_育ちで出る=int(sum(d[(s, '換算')][0] <= d[(s, '換算')][1] / 2 for s in S)),
               H3_元に負けない=int(sum(d[(s, '換算')][1] >= d[(s, '元')][1] for s in S)), 参考_元の差が育つ=int(sum(差(s, '元', 1) > 差(s, '元', 0) for s in S)))
    res['判定'] = {k: res[k] >= 8 for k in ['H1_差が育つ', 'H2_育ちで出る', 'H3_元に負けない']}
    res['中央値'] = {a: [round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in range(2)] for a in ['道具', '元', '換算']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
