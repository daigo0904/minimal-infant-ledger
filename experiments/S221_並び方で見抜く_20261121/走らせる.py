import sys, json, numpy as np
sys.path.insert(0, '../S221_並び方で見抜く_20261121')
from multiprocessing import Pool
腕 = {'嘘つき・差の信用': (True, True), '嘘つき・並びの信用': (True, '並び'), '嘘つきなし': (False, False)}
def one(job):
    import 数え; s, 名 = job; u, c = 腕[名]; return (s, 名) + tuple(数え.測る(s, 嘘=u, 信用=c))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(45800, 45830) if 段 == '本' else range(45900, 45930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 90; v = lambda s, 名, k: d[(s, 名)][k]
    A, B, N = '嘘つき・並びの信用', '嘘つき・差の信用', '嘘つきなし'
    res = {'H1_並びで嘘つきをもっと疑う': int(sum(v(s, A, 2) < v(s, B, 2) for s in S)), 'H2_並びで得が戻る': int(sum(v(s, A, 0) > v(s, B, 0) for s in S)), 'H3_害が消える': int(sum(v(s, A, 0) >= v(s, N, 0) for s in S)), 'H4_正直は疑わない': int(sum(v(s, A, 3) > 0.5 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['参考_表の相関_並び>嘘つきなし'] = int(sum(v(s, A, 1) > v(s, N, 1) for s in S))
    res['中央値'] = {名: dict(得=round(float(np.median([v(s, 名, 0) for s in S])), 4), 表の相関=round(float(np.median([v(s, 名, 1) for s in S])), 3), 嘘つきへの信用=round(float(np.median([v(s, 名, 2) for s in S])), 3), 正直への信用=round(float(np.median([v(s, 名, 3) for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
