import sys, json, numpy as np
sys.path.insert(0, '../S156_値打ちか選び方か_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 正直 = job; return (s, 正直) + 数える(一生(s, '養育者', 物知り=(1, 正直), 記録=True), s, (1, 正直))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(33600, 33630) if 段 == '本' else range(33700, 33730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 正直) for 正直 in [1.0, 0.7] for s in S], chunksize=1)
    d = {(s, 正直): v for s, 正直, *v in r}; assert len(d) == 60
    比 = lambda s, j: d[(s, 0.7)][j] / d[(s, 1.0)][j]
    res = {'H1_顔ごとは比例': sum(比(s, 1) > 0.28 for s in S), 'H2_正体ごとは二乗': sum(比(s, 0) < 0.28 for s in S), 'H3_食べ予測も比例': sum(比(s, 3) > 0.28 for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['比の中央値'] = {n: round(float(np.median([比(s, j) for s in S])), 3) for j, n in enumerate(['正体ごと', '顔ごと', '余裕', '食べ予測', '癖'])}
    res['差の中央値'] = {f'{正直}': [round(float(np.median([d[(s, 正直)][j] for s in S])), 3) for j in range(5)] for 正直 in [1.0, 0.7]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
