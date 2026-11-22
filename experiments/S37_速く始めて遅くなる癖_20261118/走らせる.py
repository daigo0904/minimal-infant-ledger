import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
def 予定(t): return 0.05 + (0.01 - 0.05) * min(t, 4000) / 4000
記録 = []
class 下げる(B.換算):
    """赤ちゃんの手数で Q の学び率を決める：0〜4000手で 0.05→0.01、その後 0.01"""
    def __init__(s, *a): super().__init__(*a); s.手数 = 0
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        s.手数 += 1; W.学び率 = 予定(s.手数)
        if s.手数 == 2000: 記録.append(W.学び率)
        try: return super().受ける(φ, a, q, e, 食べた, 我慢)
        finally: W.学び率 = 0.05
def 一生(s, 腕, 寿命=8000):
    W.赤ちゃん = 下げる if 腕 == '下げる' else B.換算; W.学び率 = 0.01 if 腕 == '0.01' else 0.05
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.赤ちゃん = B.原; W.学び率 = 0.05
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, [float(np.mean([B.区(o, 7000, 7500)[j], B.区(o, 7500, 8000)[j]])) for j in range(3)], float(o['h列'][70:80].mean()))
腕 = ['0.05', '0.01', '下げる']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(10899, a, 2100)['sha256'] for a in 腕]; print('3腕が互いに違う:', len(set(x)) == 3, ' 2000手目の学び率:', sorted(set(round(v, 4) for v in 記録))); sys.exit()
    段 = sys.argv[1]; S = range(10800, 10810) if 段 == '本' else range(10900, 10910)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): (g, h) for s, a, g, h in r}
    res = dict(H1_漏れが減る=int(sum(d[(s, '下げる')][0][1] < d[(s, '0.05')][0][1] for s in S)), H2_空腹が遅いより大きくない=int(sum(d[(s, '下げる')][1] <= d[(s, '0.01')][1] for s in S)),
               H3_見られ分けは負けない=int(sum(d[(s, '下げる')][0][2] >= d[(s, '0.05')][0][2] for s in S)))
    res['判定'] = {k: v >= 8 for k, v in res.items()}
    res['中央値'] = {a: dict(育_P養P他差=[round(float(np.median([d[(s, a)][0][j] for s in S])), 3) for j in range(3)], 空腹=round(float(np.median([d[(s, a)][1] for s in S])), 3)) for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
