import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
窓 = [None]
class 切れる(B.換算):
    """窓[0]=(lo,hi) の手（1始まりの手数で lo<手数≤hi）だけ、つながりの項を切って Q だけで選ぶ（学びはそのまま）"""
    def __init__(s, *a): super().__init__(*a); s.手数 = 0
    def 選ぶ(s, φ):
        s.手数 += 1
        if 窓[0] and 窓[0][0] < s.手数 <= 窓[0][1]:
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); a = int(np.argmax(q))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        return super().選ぶ(φ)
def 一生(s, v, 切, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = v; W.赤ちゃん = 切れる; 窓[0] = 切
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; W.赤ちゃん = B.原; B.v時定数 = 1000.0; 窓[0] = None
def one(job):
    s, v = job
    A = 一生(s, v, None); Bk = 一生(s, v, (0, 500)); C = 一生(s, v, (7000, 8000))
    assert (A['行動列'][:7000] == C['行動列'][:7000]).all()
    育 = lambda o: float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]]))
    return (s, v, B.区(A, 0, 500)[2] - B.区(Bk, 0, 500)[2], 育(A) - 育(C), B.区(A, 0, 500)[2], 育(A))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        A = 一生(11899, 5000.0, None, 7300); Bk = 一生(11899, 5000.0, (0, 500), 7300); C = 一生(11899, 5000.0, (7000, 8000), 7300)
        print('B は 0〜500 で違う:', bool((A['行動列'][:500] != Bk['行動列'][:500]).any()), ' C は 7000手まで同じ:', bool((A['行動列'][:7000] == C['行動列'][:7000]).all()), ' C は 7000〜 で違う:', bool((A['行動列'][7000:] != C['行動列'][7000:]).any()))
        print('v1000≠v5000:', 一生(11899, 1000.0, None, 600)['sha256'] != 一生(11899, 5000.0, None, 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(11800, 11830) if 段 == '本' else range(11900, 11930)
    with Pool(8) as p: r = p.map(one, [(s, v) for v in [1000.0, 5000.0] for s in S])
    d = {(s, v): (e0, e1, a0, a1) for s, v, e0, e1, a0, a1 in r}
    res = dict(H1_効きが育つ=int(sum(d[(s, 5000.0)][1] > d[(s, 5000.0)][0] for s in S)),
               H2_育ちが1000より大きい=int(sum(d[(s, 5000.0)][1] - d[(s, 5000.0)][0] > d[(s, 1000.0)][1] - d[(s, 1000.0)][0] for s in S)),
               参考_1000で効きが育つ=int(sum(d[(s, 1000.0)][1] > d[(s, 1000.0)][0] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_効きが育つ', 'H2_育ちが1000より大きい']}
    res['中央値'] = {str(int(v)): dict(効き_初め=round(float(np.median([d[(s, v)][0] for s in S])), 3), 効き_育=round(float(np.median([d[(s, v)][1] for s in S])), 3),
                                    見られ分け_初め=round(float(np.median([d[(s, v)][2] for s in S])), 3), 見られ分け_育=round(float(np.median([d[(s, v)][3] for s in S])), 3)) for v in [1000.0, 5000.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
