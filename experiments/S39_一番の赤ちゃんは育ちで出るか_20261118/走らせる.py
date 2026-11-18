import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
def 一生(s, 腕, 寿命=8000):
    W.学び率 = 0.01; W.赤ちゃん = B.換算 if 腕 == '一番' else B.原
    try: return W.一生(s, '依存', '獲得型' if 腕 == '一番' else '道具型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; W.赤ちゃん = B.原
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, B.区(o, 0, 500)[2], float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]])), [B.区(o, k, k + 500)[2] for k in range(0, 8000, 500)])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        print('一番≠道具:', 一生(11299, '一番', 600)['sha256'] != 一生(11299, '道具', 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(11200, 11230) if 段 == '本' else range(11300, 11330)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['一番', '道具'] for s in S])
    d = {(s, a): (f, g, t) for s, a, f, g, t in r}
    res = dict(H1_育ちで出る=int(sum(d[(s, '一番')][0] <= d[(s, '一番')][1] / 2 for s in S)),
               H2_道具との差が育つ=int(sum(d[(s, '一番')][1] - d[(s, '道具')][1] > d[(s, '一番')][0] - d[(s, '道具')][0] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(初め=round(float(np.median([d[(s, a)][0] for s in S])), 3), 育った後=round(float(np.median([d[(s, a)][1] for s in S])), 3), 推移=[round(float(np.median([d[(s, a)][2][k] for s in S])), 3) for k in range(16)]) for a in ['一番', '道具']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
