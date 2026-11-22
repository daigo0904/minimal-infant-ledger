import sys, json, numpy as np
sys.path.insert(0, '../S147_社会的参照_20261120')
from multiprocessing import Pool
from 共 import *
腕 = [('養育者', 'v3'), ('ずらし', 'v3'), ('養育者', '元')]
def one(job): s, 参照, 名 = job; o = 一生(s, 参照, 名); return (s, 参照, 名) + 数える(o, 0, 1000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(32400, 32430) if 段 == '本' else range(32500, 32530)
    with Pool(8) as p: r = p.map(one, [(s, a, b) for a, b in 腕 for s in S])
    d = {(s, a, b): v for s, a, b, *v in r}
    V3, Z, 元_ = lambda s: d[(s, '養育者', 'v3')], lambda s: d[(s, 'ずらし', 'v3')], lambda s: d[(s, '養育者', '元')]
    res = {'H1_養育者の表情に従うことが育つ（v3）': int(sum(V3(s)[4] > V3(s)[0] for s in S)), 'H2_本物の表情でだけ（v3 本物>ずらし）': int(sum(V3(s)[4] > Z(s)[4] for s in S)),
           'H3_仲間の表情より養育者の表情に従う（v3）': int(sum(V3(s)[4] > V3(s)[5] for s in S)), 'H4_v3 は元の頭より従う': int(sum(V3(s)[4] > 元_(s)[4] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_養育者に従う', '初め_仲間に従う', '初め_仲間の前の物の差', '初め_食べ', '終わり_養育者に従う', '終わり_仲間に従う', '終わり_仲間の前の物の差', '終わり_食べ']
    res['中央値'] = {f'{a}_{b}': {n: round(float(np.median([d[(s, a, b)][j] for s in S])), 3) for j, n in enumerate(名)} for a, b in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
