import sys, json, numpy as np
from collections import deque
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
ずらし幅 = [1]
直前の食 = {}
class 偽窓(deque):
    """つながりの学びに渡す『食べた』だけを差し替える窓（append された値の代わりに 偽値 を入れる）"""
    偽値 = 0.0
    def append(self, x): super().append(self.偽値)
class ずらし(B.換算):
    """つながりの学びだけ、隣の子(i+1)が1手前に食べたか にする。行動・空腹・Q・v食 は本物の食べ物。幅0なら本物"""
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; s.食窓 = 偽窓()
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        偽 = 直前の食.get((s.番 + 1) % 8, False) if ずらし幅[0] else 食べた
        直前の食[s.番] = 食べた
        s.食窓.偽値 = 1.0 if 偽 else 0.0
        return super().受ける(φ, a, q, e, 食べた, 我慢)
def 一生(s, 腕, 寿命=8000, 幅=1):
    W.学び率 = 0.01; B.v時定数 = 5000.0; ずらし幅[0] = 幅; 直前の食.clear()
    W.赤ちゃん = ずらし if 腕 == 'ずらし' else B.換算
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.赤ちゃん = B.原
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, B.区(o, 0, 500)[2], float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]])))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(12899, '本物', 1500); b = 一生(12899, 'ずらし', 1500, 幅=0); c = 一生(12899, 'ずらし', 1500, 幅=1)
        print('幅0で本物と同じ:', a['sha256'] == b['sha256'], ' 幅1で違う:', a['sha256'] != c['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(12800, 12830) if 段 == '本' else range(12900, 12930)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['本物', 'ずらし'] for s in S])
    d = {(s, a): (f, g) for s, a, f, g in r}
    res = dict(H1_育った後で本物が大きい=int(sum(d[(s, '本物')][1] > d[(s, 'ずらし')][1] for s in S)),
               H2_育ちが本物で大きい=int(sum(d[(s, '本物')][1] - d[(s, '本物')][0] > d[(s, 'ずらし')][1] - d[(s, 'ずらし')][0] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: [round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in range(2)] for a in ['本物', 'ずらし']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
