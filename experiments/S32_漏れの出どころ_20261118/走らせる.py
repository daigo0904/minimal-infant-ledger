import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30 の換算型と S16 世界（感覚256・雑音0.3）
W = B.W
切り始め = 7000
切る = [False]
class 切れる(B.換算):
    """7000手目からつながりの項を切って Q だけで選ぶ（学びはそのまま）"""
    def __init__(s, *a): super().__init__(*a); s.手数 = 0
    def 選ぶ(s, φ):
        s.手数 += 1
        if 切る[0] and s.手数 > 切り始め:
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); a = int(np.argmax(q))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        return super().選ぶ(φ)
def 一生(s, 切, 寿命=8000):
    切る[0] = 切; W.赤ちゃん = 切れる
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.赤ちゃん = B.原
def one(job):
    s, 切 = job; o = 一生(s, 切); return (s, 切, B.区(o, 7000, 8000), o['行動列'])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = one((9899, False)); b = one((9899, True))
        print('7000手まで同じ:', bool((a[3][:7000] == b[3][:7000]).all()), ' 7000手から違う:', bool((a[3][7000:] != b[3][7000:]).any()))
        sys.path.insert(0, '../S31_組み合わせの効き_20261118')
        print('切らない腕＝S30 の換算×その手だけ:', bool((a[3] == B.一生(9899, 'その手だけ')['行動列']).all())); sys.exit()
    段 = sys.argv[1]; S = range(9800, 9810) if 段 == '本' else range(9900, 9910)
    with Pool(8) as p: r = p.map(one, [(s, k) for k in [False, True] for s in S])
    for x in r: assert (x[3][:7000] == [y for y in r if y[0] == x[0] and y[1] != x[1]][0][3][:7000]).all()
    d = {(s, k): v for s, k, v, _ in r}
    res = dict(H1_漏れはQから=int(sum(d[(s, True)][1] >= 0.9 * d[(s, False)][1] for s in S)), H2_切るとP養が下がる=int(sum(d[(s, True)][0] < d[(s, False)][0] for s in S)))
    res['判定'] = {k: v >= 8 for k, v in res.items()}
    res['中央値_P養P他差'] = {('切る' if k else '切らない'): [round(float(np.median([d[(s, k)][j] for s in S])), 3) for j in range(3)] for k in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=[(s, k, v) for s, k, v, _ in r]), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
