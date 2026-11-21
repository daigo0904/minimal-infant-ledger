import sys, json, numpy as np
sys.path.insert(0, '../S227_言葉が要る世界_20261121')
from multiprocessing import Pool
腕 = {'本': (50.0, False), '聞き手も見える': (50.0, True), '共感なし': (0.0, False)}
def one(job):
    import 数え; s, 名 = job; k, v = 腕[名]; return (s, 名) + tuple(数え.測る(s, k, v))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(47000, 47030) if 段 == '本' else range(47100, 47130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 90; v = lambda s, 名, k: d[(s, 名)][k]
    res = {'H1_偶然より当たる': int(sum(v(s, '本', 0) > 0.30 for s in S)), 'H2_要る世界のほうが合図に意味': int(sum(v(s, '本', 1) > v(s, '聞き手も見える', 1) for s in S)), 'H3_共感のおかげで合図に意味': int(sum(v(s, '本', 1) > v(s, '共感なし', 1) for s in S)), 'H4_共感のおかげで当たる': int(sum(v(s, '本', 0) > v(s, '共感なし', 0) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {名: dict(当たり=round(float(np.median([v(s, 名, 0) for s in S])), 3), 結びつき=round(float(np.median([v(s, 名, 1) for s in S])), 3), 空腹=round(float(np.median([v(s, 名, 2) for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
