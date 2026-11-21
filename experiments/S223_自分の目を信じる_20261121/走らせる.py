import sys, json, numpy as np
sys.path.insert(0, '../S223_自分の目を信じる_20261121')
from multiprocessing import Pool
腕 = {'悪口・ふるいなし': (True, None, 0.05), '悪口・ふるい0.05': (True, 0.05, 0.05), '悪口なし・ふるい0.05': (False, 0.05, 0.05), '悪口なし・噂なし': (False, None, 0.0)}
def one(job):
    import 数え; s, 名 = job; a, f, g = 腕[名]; return (s, 名) + tuple(数え.測る(s, 悪=a, ふるい=f, 噂=g))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(46200, 46230) if 段 == '本' else range(46300, 46330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 120; v = lambda s, 名, k: d[(s, 名)][k]
    A, N, B, Z = '悪口・ふるい0.05', '悪口・ふるいなし', '悪口なし・ふるい0.05', '悪口なし・噂なし'
    res = {'H1_ふるいで標的の損が減る': int(sum(v(s, A, 0) < v(s, N, 0) for s in S)), 'H2_ふるいで標的の評判が戻る': int(sum(v(s, A, 2) > v(s, N, 2) for s in S)), 'H3_ふるいは正直な噂を壊さない': int(sum(v(s, B, 3) >= v(s, Z, 3) for s in S)), 'H4_ふるいで嘘つきが疑われる': int(sum(v(s, A, 1) < v(s, N, 1) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {名: dict(標的の損=round(float(np.median([v(s, 名, 0) for s in S])), 4), 嘘つきへの信用=round(float(np.median([v(s, 名, 1) for s in S])), 3), 標的の評判差=round(float(np.median([v(s, 名, 2) for s in S])), 3), 表の相関=round(float(np.median([v(s, 名, 3) for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
