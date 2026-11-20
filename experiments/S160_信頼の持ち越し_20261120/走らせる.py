import sys, json, numpy as np
sys.path.insert(0, '../S160_信頼の持ち越し_20261120')
from multiprocessing import Pool
from 共 import *
G2 = (4000, 0.9)
def one(job):
    s, 正直 = job; o = 一生(s, '養育者', 物知り=(1, 正直), 合図2=G2)
    return (s, 正直, 数える(o, s, (1, 正直), 3000, 4000)[1], 合図2の差(o, s, G2, 4000, 5000), 合図2の差(o, s, G2, 7000, 8000), 合図2の差(o, s, G2, 7000, 8000, 3), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(34400, 34430) if 段 == '本' else range(34500, 34530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 正直) for 正直 in [1.0, 0.5] for s in S], chunksize=1)
    d = {(s, 正直): v for s, 正直, *v in r}; assert len(d) == 60
    res = {'H1_持ち越し': sum(d[(s, 1.0)][1] > d[(s, 0.5)][1] for s in S), 'H2_誰でも学ぶ': sum(d[(s, 0.5)][2] > 0 for s in S),
           '対照_物知りの合図だけ': sum(abs(d[(s, 1.0)][3]) < d[(s, 1.0)][2] for s in S), 'sha違う': sum(d[(s, 1.0)][4] != d[(s, 0.5)][4] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_持ち越し', 'H2_誰でも学ぶ', '対照_物知りの合図だけ']}
    res['中央値'] = {f'{正直}': dict(zip(['前半終わり表情', '後半初め合図2', '後半終わり合図2', 'ほかの仲間の前'], [round(float(np.median([d[(s, 正直)][j] for s in S])), 3) for j in range(4)])) for 正直 in [1.0, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
