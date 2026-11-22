import json, sys, numpy as np
import 頭 as H
from multiprocessing import Pool
W = H.W
def one(job):
    s, h, w = job; W.重み = w; o = H.一生(s, h); f, g, _ = H.数字(o); return (s, h, w, f, g, o['sha256'])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        W.重み = 2.0; a = H.一生(8499, '獲得型', 寿命=800); W.重み = 0.0001; b = H.一生(8499, '獲得型', 寿命=800)
        print('重みで違う一生:', a['sha256'] != b['sha256']); sys.exit(0)
    段 = sys.argv[1]; 種 = range(8400, 8410) if 段 == '本' else range(8500, 8510)
    腕 = [('獲得型', 2.0), ('獲得型', 0.0001), ('道具型', 2.0)]
    with Pool(8) as p: r = p.map(one, [(s, h, w) for h, w in 腕 for s in 種])
    d = {(s, h, w): (f, g) for s, h, w, f, g, _ in r}
    T = lambda s: d[(s, '道具型', 2.0)]
    res = dict(H1_同点くずし=sum(d[(s, '獲得型', 0.0001)][0] - T(s)[0] >= 0.5 * (d[(s, '獲得型', 2.0)][0] - T(s)[0]) for s in 種),
               H2_大きさは育った後=sum(d[(s, '獲得型', 2.0)][1] > d[(s, '獲得型', 0.0001)][1] for s in 種))
    res['判定'] = {k: res[k] >= 8 for k in ['H1_同点くずし', 'H2_大きさは育った後']}
    res['中央値'] = {f'{h}{w}': dict(初め=round(float(np.median([d[(s, h, w)][0] for s in 種])), 3), 育った後=round(float(np.median([d[(s, h, w)][1] for s in 種])), 3)) for h, w in 腕}
    print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=[dict(種=s, 頭=h, 重み=w, 初め=f, 育=g, sha=x) for s, h, w, f, g, x in r]), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
