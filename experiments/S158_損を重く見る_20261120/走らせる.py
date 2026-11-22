import sys, json, numpy as np
sys.path.insert(0, '../S158_損を重く見る_20261120')
from multiprocessing import Pool
from 共 import *
腕 = {'ずっと1.0': (1, 1.0), '1.0→0.5': (1, 1.0, 0.5, 4000), 'ずっと0.5': (1, 0.5), '0.5→1.0': (1, 0.5, 1.0, 4000)}
def one(job): s, 名, w = job; o = 一生(s, '養育者', 物知り=腕[名], 記録=True, 損重さ=w); return (s, 名, w) + 数える(o, s, 腕[名], 6000, 8000) + (float(o['食列'][6000:].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(34000, 34030) if 段 == '本' else range(34100, 34130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名, w) for w in [1.0, 3.0] for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名, w): v for s, 名, w, *v in r}; assert len(d) == 240
    f = lambda s, 名, w: d[(s, 名, w)][1]
    失 = lambda s, w: f(s, 'ずっと1.0', w) - f(s, '1.0→0.5', w); 得 = lambda s, w: f(s, '0.5→1.0', w) - f(s, 'ずっと0.5', w)
    res = {'H1_損重さ3で失うほうが早い': sum(失(s, 3.0) > 得(s, 3.0) for s in S), 'H2_偏りが増える': sum(失(s, 3.0) - 得(s, 3.0) > 失(s, 1.0) - 得(s, 1.0) for s in S),
           'H3_早く失う': sum(失(s, 3.0) > 失(s, 1.0) for s in S), '参考_損重さ1で失うほうが早い': sum(失(s, 1.0) > 得(s, 1.0) for s in S),
           'sha違う_損重さ': sum(d[(s, '1.0→0.5', 1.0)][6] != d[(s, '1.0→0.5', 3.0)][6] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_損重さ3で失うほうが早い', 'H2_偏りが増える', 'H3_早く失う']}
    res['中央値'] = {f'損重さ{w}': {**{名: round(float(np.median([f(s, 名, w) for s in S])), 3) for 名 in 腕}, '失う量': round(float(np.median([失(s, w) for s in S])), 3), '育つ量': round(float(np.median([得(s, w) for s in S])), 3), '食べ': round(float(np.median([d[(s, 'ずっと1.0', w)][5] for s in S])), 4)} for w in [1.0, 3.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
