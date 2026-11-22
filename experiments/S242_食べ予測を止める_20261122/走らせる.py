import sys, json, numpy as np
sys.path.insert(0, '../S242_食べ予測を止める_20261122')
from multiprocessing import Pool
腕 = {'kf3・kE50': (3.0, 50.0, True), 'kf3・kE500': (3.0, 500.0, True), 'kf0・kE50': (0.0, 50.0, True), 'kf0・kE500': (0.0, 500.0, True), '協力・kf0・kE500': (0.0, 500.0, False), '協力・kf3・kE50': (3.0, 50.0, False)}
def one(job):
    import 数え; s, 名 = job; kf, kE, c = 腕[名]; return (s, 名) + tuple(数え.測る(s, kf, kE, c))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(50000, 50030) if 段 == '本' else range(50100, 50130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 180; v = lambda s, 名, j: d[(s, 名)][j]
    res = {'H1_食べ予測を止めると強い共感で当たる': int(sum(v(s, 'kf0・kE500', 0) > v(s, 'kf3・kE500', 0) for s in S)), 'H2_言葉が戻る（>0.30）': int(sum(v(s, 'kf0・kE500', 0) > 0.30 for s in S)), 'H3_kf0で共感が効く': int(sum(v(s, 'kf0・kE500', 0) > v(s, 'kf0・kE50', 0) for s in S)), 'H4_協力でもkf0なら言葉ができない（<0.30）': int(sum(v(s, '協力・kf0・kE500', 0) < 0.30 for s in S)), 'H5_協力でもkf0なら話し手の言い方が消える': int(sum(v(s, '協力・kf0・kE500', 2) < v(s, '協力・kf3・kE50', 2) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {名: dict(当たり=round(float(np.median([v(s, 名, 0) for s in S])), 3), 全体=round(float(np.median([v(s, 名, 1) for s in S])), 3), 話し手ごと=round(float(np.median([v(s, 名, 2) for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
