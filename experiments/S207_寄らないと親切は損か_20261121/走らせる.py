import sys, json, numpy as np
sys.path.insert(0, '../S207_寄らないと親切は損か_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(43000, 43030) if 段 == '本' else range(43100, 43130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k, g) for g in [1.0, 0.0] for k in [1.0, 3.0] for s in S], chunksize=1)
    d = {(s, k, g): v for s, k, g, *v in r}; assert len(d) == 120
    D = lambda s, g, j: d[(s, 3.0, g)][j] - d[(s, 1.0, g)][j]
    res = {'H1_寄らないと損_感謝なし': int(sum(D(s, 0.0, 2) > 0 for s in S)), 'H2_寄らないと損_感謝あり': int(sum(D(s, 1.0, 2) > 0 for s in S)),
           'H3_感謝で返る': int(sum(D(s, 1.0, 0) > D(s, 0.0, 0) for s in S)), 'H4_感謝で損が小さい': int(sum(D(s, 0.0, 2) > D(s, 1.0, 2) for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kG{g}': dict(zip(['なぐさめてもらった', '入り次数', '空腹', '食べ', 'なぐさめた'], [round(float(np.median([D(s, g, j) for s in S])), 4) for j in range(5)])) for g in [1.0, 0.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
