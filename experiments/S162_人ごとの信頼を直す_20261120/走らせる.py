import sys, json, numpy as np
sys.path.insert(0, '../S162_人ごとの信頼を直す_20261120')
from multiprocessing import Pool
from 共 import *
G2 = (4000, 0.9)
def one(job):
    s, 正直, k = job; o = 一生(s, '養育者', 物知り=(1, 正直), 合図2=G2, kτ=k, 物知り率=0.5, 信型='一致')
    return (s, 正直, k, 数える(o, s, (1, 正直), 3000, 4000)[1], 合図2の差(o, s, G2, 4000, 5000), 合図2の差(o, s, G2, 7000, 8000), float(o['食列'].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(34600, 34630) if 段 == '本' else range(34700, 34730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 正直, k) for k in [0.0, 50.0] for 正直 in [1.0, 0.5] for s in S], chunksize=1)
    d = {(s, 正直, k): v for s, 正直, k, *v in r}; assert len(d) == 120
    g = lambda s, 正直, k: d[(s, 正直, k)][1]
    res = {'H1_持ち越し_kτ50': sum(g(s, 1.0, 50.0) > g(s, 0.5, 50.0) for s in S), 'H2_τのおかげ': sum(g(s, 1.0, 50.0) - g(s, 0.5, 50.0) > g(s, 1.0, 0.0) - g(s, 0.5, 0.0) for s in S),
           '参考_kτ0で1.0>0.5': sum(g(s, 1.0, 0.0) > g(s, 0.5, 0.0) for s in S), 'sha違う_kτ': sum(d[(s, 1.0, 0.0)][4] != d[(s, 1.0, 50.0)][4] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_持ち越し_kτ50', 'H2_τのおかげ']}
    res['中央値'] = {f'kτ{k}_{正直}': dict(zip(['前半終わり表情', '後半初め合図2', '後半終わり合図2', '食べ'], [round(float(np.median([d[(s, 正直, k)][j] for s in S])), 4) for j in range(4)])) for k in [0.0, 50.0] for 正直 in [1.0, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
