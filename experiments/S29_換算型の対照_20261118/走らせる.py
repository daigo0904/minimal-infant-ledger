import json, sys, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S28_換算型_20261118')
import 頭 as H
W = H.W
def 生(s, 世界, 換算する, 寿命=8000):
    H.c[0] = 30.0; W.赤ちゃん = H.換算 if 換算する else H.原
    try: return W.一生(s, 世界, '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = H.原
def P他(o):
    A, 相, b = o['行動列'][7000:8000], o['相手列'][7000:8000], o['一番']
    return float(np.mean([(A[:, i][相[:, i] > 0] == b).mean() for i in range(8)]))
def one(job):
    s, 世界, 換 = job; o = 生(s, 世界, 換); f, g = H.数字(o); return (s, 世界, 換, f, g, P他(o))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 生(9299, '依存', True, 600); b = 生(9299, '無関係', True, 600); c = 生(9299, '依存', False, 600)
        print('依存と無関係で違う:', a['sha256'] != b['sha256'], '換算と元で違う:', a['sha256'] != c['sha256']); sys.exit(0)
    段 = sys.argv[1]; S = range(9200, 9210) if 段 == '本' else range(9300, 9310)
    腕 = [('依存', True), ('無関係', True), ('依存', False)]
    with Pool(8) as p: r = p.map(one, [(s, w, k) for w, k in 腕 for s in S])
    d = {(s, w, k): (f, g, x) for s, w, k, f, g, x in r}
    res = dict(H1_無関係は小さい=int(sum(d[(s, '無関係', True)][1] < d[(s, '依存', True)][1] for s in S)),
               H2_育ちで出る=int(sum(d[(s, '依存', True)][0] <= d[(s, '依存', True)][1] / 2 for s in S)),
               H3_漏れが増えない=int(sum(d[(s, '依存', True)][2] <= d[(s, '依存', False)][2] for s in S)))
    res['判定'] = {k: res[k] >= 8 for k in ['H1_無関係は小さい', 'H2_育ちで出る', 'H3_漏れが増えない']}
    res['中央値'] = {f'{w}_{"換算" if k else "元"}': dict(初め=round(float(np.median([d[(s, w, k)][0] for s in S])), 3), 育った後=round(float(np.median([d[(s, w, k)][1] for s in S])), 3), P他=round(float(np.median([d[(s, w, k)][2] for s in S])), 3)) for w, k in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
