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
def 一生(s, v, 切, 寿命=8000, 世界='依存'):
    W.学び率 = 0.01; B.v時定数 = v; W.赤ちゃん = 切れる; 窓[0] = 切
    try: return W.一生(s, 世界, '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; W.赤ちゃん = B.原; B.v時定数 = 1000.0; 窓[0] = None
def one(job):
    s, w = job; v = 5000.0
    A = 一生(s, v, None, 世界=w); Bk = 一生(s, v, (0, 500), 世界=w); C = 一生(s, v, (7000, 8000), 世界=w)
    assert (A['行動列'][:7000] == C['行動列'][:7000]).all()
    育 = lambda o: float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]]))
    return (s, w, B.区(A, 0, 500)[2] - B.区(Bk, 0, 500)[2], 育(A) - 育(C), B.区(A, 0, 500)[2], 育(A))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        A = 一生(12099, 5000.0, None, 7300, '無関係'); Bk = 一生(12099, 5000.0, (0, 500), 7300, '無関係'); C = 一生(12099, 5000.0, (7000, 8000), 7300, '無関係')
        print('無関係: B は 0〜500 で違う:', bool((A['行動列'][:500] != Bk['行動列'][:500]).any()), ' C は 7000手まで同じ:', bool((A['行動列'][:7000] == C['行動列'][:7000]).all()), ' C は 7000〜 で違う:', bool((A['行動列'][7000:] != C['行動列'][7000:]).any()))
        print('依存≠無関係:', 一生(12099, 5000.0, None, 600, '依存')['sha256'] != 一生(12099, 5000.0, None, 600, '無関係')['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(12000, 12030) if 段 == '本' else range(12100, 12130)
    with Pool(8) as p: r = p.map(one, [(s, w) for w in ['依存', '無関係'] for s in S])
    d = {(s, w): (e0, e1, a0, a1) for s, w, e0, e1, a0, a1 in r}
    res = dict(H1_無関係では小さい=int(sum(d[(s, '無関係')][1] < d[(s, '依存')][1] for s in S)), H2_無関係では育たない=int(sum(d[(s, '無関係')][0] >= d[(s, '無関係')][1] for s in S)),
               参考_依存で育つ=int(sum(d[(s, '依存')][1] > d[(s, '依存')][0] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_無関係では小さい', 'H2_無関係では育たない']}
    res['中央値'] = {w: dict(効き_初め=round(float(np.median([d[(s, w)][0] for s in S])), 3), 効き_育=round(float(np.median([d[(s, w)][1] for s in S])), 3),
                            見られ分け_初め=round(float(np.median([d[(s, w)][2] for s in S])), 3), 見られ分け_育=round(float(np.median([d[(s, w)][3] for s in S])), 3)) for w in ['依存', '無関係']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
