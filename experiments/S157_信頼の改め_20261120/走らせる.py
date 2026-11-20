import sys, json, numpy as np
sys.path.insert(0, '../S157_信頼の改め_20261120')
from multiprocessing import Pool
from 共 import *
腕 = {'ずっと1.0': (1, 1.0), '1.0→0.5': (1, 1.0, 0.5, 4000), 'ずっと0.5': (1, 0.5), '0.5→1.0': (1, 0.5, 1.0, 4000)}
def one(job): s, 名 = job; o = 一生(s, '養育者', 物知り=腕[名], 記録=True); return (s, 名) + 数える(o, s, 腕[名], 6000, 8000) + (o['sha256'],)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(33800, 33830) if 段 == '本' else range(33900, 33930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 120
    f = lambda s, 名: d[(s, 名)][1]
    res = {'H1_裏切られると下がる': sum(f(s, '1.0→0.5') < f(s, 'ずっと1.0') for s in S), 'H2_正直になると育つ': sum(f(s, '0.5→1.0') > f(s, 'ずっと0.5') for s in S),
           'H3_改めきる': sum(f(s, '1.0→0.5') < (f(s, 'ずっと1.0') + f(s, 'ずっと0.5')) / 2 for s in S),
           'H4_失うほうが早い': sum(f(s, 'ずっと1.0') - f(s, '1.0→0.5') > f(s, '0.5→1.0') - f(s, 'ずっと0.5') for s in S),
           'sha違う_1.0と1.0→0.5': sum(d[(s, 'ずっと1.0')][5] != d[(s, '1.0→0.5')][5] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_裏切られると下がる', 'H2_正直になると育つ', 'H3_改めきる', 'H4_失うほうが早い']}
    res['顔ごとの取る差の中央値'] = {名: round(float(np.median([f(s, 名) for s in S])), 3) for 名 in 腕}
    res['食べ予測の差の中央値'] = {名: round(float(np.median([d[(s, 名)][3] for s in S])), 3) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
