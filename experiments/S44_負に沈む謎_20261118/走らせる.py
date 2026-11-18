import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S16 世界（感覚256・雑音0.3）
W = B.W
def 一生(s, 代価, 寿命=8000):
    W.学び率 = 0.01; W.我慢の代価 = 代価; W.赤ちゃん = B.原
    try: return W.一生(s, '無関係', '道具型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; W.我慢の代価 = 0.01
def one(job):
    s, c = job; o = 一生(s, c)
    return (s, c, B.区(o, 0, 500)[2], [float(np.mean([B.区(o, 7000, 7500)[j], B.区(o, 7500, 8000)[j]])) for j in range(3)])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        print('代価0≠0.01:', 一生(12299, 0.0, 600)['sha256'] != 一生(12299, 0.01, 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(12200, 12230) if 段 == '本' else range(12300, 12330)
    with Pool(8) as p: r = p.map(one, [(s, c) for c in [0.01, 0.0] for s in S])
    d = {(s, c): g for s, c, f, g in r}
    res = dict(H1_負が消える=int(sum(d[(s, 0.0)][2] > d[(s, 0.01)][2] for s in S)), H2_代価0はほぼ0以上=int(sum(d[(s, 0.0)][2] >= -0.02 for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値_育_P養P他差'] = {str(c): [round(float(np.median([d[(s, c)][j] for s in S])), 3) for j in range(3)] for c in [0.01, 0.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
