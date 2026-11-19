import sys, json, numpy as np
sys.path.insert(0, '../S109_共同注意_20261119')
from multiprocessing import Pool
import 共通2 as C
B, W, N = C.B, C.W, C.N
設定 = dict(窓=None, 型='そのまま')
class 窓切り(B.換算):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.手数 = 0
    def 選ぶ(s, φ):
        t = s.手数; s.手数 += 1
        if 設定['窓'] is None or not (設定['窓'][0] <= t < 設定['窓'][1]) or 設定['型'] == 'そのまま': return super().選ぶ(φ)
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ); つ = B.c * max(s.v食, 0.0) * u * ê
        score = q if 設定['型'] == 'Qだけ' else つ
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
def 一生(s, 型, 寿命=8000):
    設定['窓'] = (7000, 8000); 設定['型'] = 型; 原 = B.換算; B.換算 = 窓切り
    try: return C.一生(s, 4, '本物', 寿命=寿命, 学び率=0.01)
    finally: B.換算 = 原; 設定['窓'] = None
def one(job):
    s, 型 = job; o = 一生(s, 型); return (s, 型) + C.追う(o, 7000, 8000) + C.追う(o, 6000, 7000)
腕 = ['そのまま', 'Qだけ', 'つながりだけ']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 26599; y = {型: 一生(s, 型) for 型 in 腕}
        S109 = C.一生(s, 4, '本物', 学び率=0.01)['sha256']; print('そのまま は S109 と同じ sha:', y['そのまま']['sha256'] == S109)
        print('7000 までの手は3腕で同じ:', all((y[a]['行動列'][:7000] == y['そのまま']['行動列'][:7000]).all() for a in 腕), ' 7000〜 は違う:', len({y[a]['sha256'] for a in 腕}) == 3)
        print({a: [round(v, 3) for v in one((s, a))[2:]] for a in 腕}); sys.exit()
    段 = sys.argv[1]; S = range(26400, 26430) if 段 == '本' else range(26500, 26530)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): v for s, a, *v in r}
    res = {'H1_視線追いは癖から（Qだけ>つながりだけ）': int(sum(d[(s, 'Qだけ')][0] > d[(s, 'つながりだけ')][0] for s in S)),
           'H2_Qだけでもほぼ保つ（そのまま−0.03 以上）': int(sum(d[(s, 'Qだけ')][0] >= d[(s, 'そのまま')][0] - 0.03 for s in S)),
           'H3_つながりだけでは偶然並み（0.30 未満）': int(sum(d[(s, 'つながりだけ')][0] < 0.30 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(窓の養育者の視線=round(float(np.median([d[(s, a)][0] for s in S])), 3), 窓の仲間の視線=round(float(np.median([d[(s, a)][1] for s in S])), 3), 窓の前の養育者=round(float(np.median([d[(s, a)][2] for s in S])), 3)) for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
