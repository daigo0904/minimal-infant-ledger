import sys, json, numpy as np
sys.path.insert(0, '../S153_表情の信頼性_20261120')
from multiprocessing import Pool
from 共 import *
def one(job): s, 正直 = job; o = 一生(s, '養育者', 'v4', 物知り=(1, 正直)); return (s, 正直) + 数える(o, 0, 2000) + 数える(o, 6000, 8000)
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(33000, 33030) if 段 == '本' else range(33100, 33130)
    with Pool(8) as p: r = p.map(one, [(s, 正直) for 正直 in [1.0, 0.7, 0.5] for s in S])
    d = {(s, 正直): v for s, 正直, *v in r}
    res = {'H1_正直な物知りほど従う（1.0>0.7）': int(sum(d[(s, 1.0)][5] > d[(s, 0.7)][5] for s in S)), 'H2_7割正直でもほかの仲間より従う': int(sum(d[(s, 0.7)][5] > d[(s, 0.7)][6] for s in S)),
           'H3_7割正直は5割（でたらめ）より従う': int(sum(d[(s, 0.7)][5] > d[(s, 0.5)][5] for s in S)), 'H4_養育者には従い続ける（0.7 の世界で 養育者>物知り）': int(sum(d[(s, 0.7)][4] > d[(s, 0.7)][5] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'正直さ{正直}': dict(養育者=round(float(np.median([d[(s, 正直)][4] for s in S])), 3), 物知り=round(float(np.median([d[(s, 正直)][5] for s in S])), 3), ほかの仲間=round(float(np.median([d[(s, 正直)][6] for s in S])), 3)) for 正直 in [1.0, 0.7, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
