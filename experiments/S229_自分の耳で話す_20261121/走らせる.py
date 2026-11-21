import sys, json, numpy as np
sys.path.insert(0, '../S229_自分の耳で話す_20261121')
from multiprocessing import Pool
腕 = {'ふつう': ('ふつう', 50.0, False), '耳': ('耳', 50.0, False), '耳・共感なし': ('耳', 0.0, False), '耳・聞き手も見える': ('耳', 50.0, True)}
def one(job):
    import 数え; s, 名 = job; k, e, v = 腕[名]; return (s, 名) + tuple(数え.測る(s, k, kE=e, 見える=v))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(47400, 47430) if 段 == '本' else range(47500, 47530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 120; v = lambda s, 名, j: d[(s, 名)][j]
    res = {'H1_耳で全体の結びつきが大': int(sum(v(s, '耳', 1) > v(s, 'ふつう', 1) for s in S)), 'H2_耳で当たりが大': int(sum(v(s, '耳', 0) > v(s, 'ふつう', 0) for s in S)), 'H3_耳で言い方がそろう': int(sum(v(s, '耳', 3) > v(s, 'ふつう', 3) for s in S)), 'H4_共感なしでも耳なら言葉ができる': int(sum(v(s, '耳・共感なし', 1) > v(s, 'ふつう', 1) for s in S)), 'H5_要らない世界では耳でも弱い': int(sum(v(s, '耳・聞き手も見える', 1) < v(s, '耳', 1) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {名: dict(当たり=round(float(np.median([v(s, 名, 0) for s in S])), 3), 全体の結びつき=round(float(np.median([v(s, 名, 1) for s in S])), 3), 話し手ごと=round(float(np.median([v(s, 名, 2) for s in S])), 3), 一致=round(float(np.median([v(s, 名, 3) for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
