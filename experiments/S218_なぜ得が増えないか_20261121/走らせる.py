import sys, json, numpy as np
sys.path.insert(0, '../S218_なぜ得が増えないか_20261121')
from multiprocessing import Pool
腕 = {'噂なし': ('見た', 0.0), '噂0.01': ('見た', 0.01), '共有': (False, 0.0)}
名前 = ['a_親切へ寄る割合', '受けた_親切', '受けた_親切でない', '受けた差', '親→親', '親→不', '不→親', '不→不', '得']
def one(job):
    import 数え; s, 名 = job; 私, g = 腕[名]; return (s, 名) + tuple(数え.測る(s, 私的=私, 噂=g))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(45200, 45230) if 段 == '本' else range(45300, 45330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 90; v = lambda s, 名, k: d[(s, 名)][名前.index(k)]
    res = {'H1_噂で親切へ寄る割合が上がる': int(sum(v(s, '噂0.01', 'a_親切へ寄る割合') > v(s, '噂なし', 'a_親切へ寄る割合') for s in S)), 'H2_噂で受けた差が増える': int(sum(v(s, '噂0.01', '受けた差') > v(s, '噂なし', '受けた差') for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['参考_噂0.01が噂なしより大'] = {k: int(sum(v(s, '噂0.01', k) > v(s, '噂なし', k) for s in S)) for k in 名前}
    res['中央値'] = {名: {k: round(float(np.median([v(s, 名, k) for s in S])), 4) for k in 名前} for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
