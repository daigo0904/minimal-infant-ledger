import sys, json, numpy as np
sys.path.insert(0, '../S169_見て避ける_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): return job + 測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(35600, 35630) if 段 == '本' else range(35700, 35730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in [0.0, 3.0] for s in S], chunksize=1)
    d = {(s, k): v for s, k, *v in r}; assert len(d) == 60
    res = {'H1_得に手を出す': sum(d[(s, 3.0)][0] > d[(s, 0.0)][0] for s in S), 'H2_損を避ける': sum(d[(s, 3.0)][1] < d[(s, 0.0)][1] for s in S),
           'H3_痛い目の前に避ける': sum(d[(s, 3.0)][4] > d[(s, 0.0)][4] for s in S), 'H4_見本の偏り': sum(d[(s, 0.0)][7] < 0.25 for s in S), 'sha違う': sum(d[(s, 3.0)][8] != d[(s, 0.0)][8] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_得に手を出す', 'H2_損を避ける', 'H3_痛い目の前に避ける', 'H4_見本の偏り']}
    res['中央値'] = {f'代理{k}': dict(zip(['良いを取る', '悪いを取る', '前半良い', '前半悪い', '初めて悪いまで', '悪い取り回数', '食べ', '取った中の悪い割合'], [round(float(np.median([d[(s, k)][j] for s in S])), 4) for j in range(8)])) for k in [0.0, 3.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
