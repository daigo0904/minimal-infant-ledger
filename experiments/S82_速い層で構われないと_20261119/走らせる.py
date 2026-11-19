import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
T = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
M = L('S64R', '../S64_構われないと_20261118/走らせる.py')
assert T.B is M.B or True
B, W, N = M.B, M.B.W, M.N
二層 = T.二層 if T.B is M.B else None
if 二層 is None:   # S81 の頭は別の読み込みの B の上にあるので、同じ中身を S64 の B の上に作り直す
    class 二層(B.換算):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.F = np.zeros(W.行動数)
        def 選ぶ(s, φ):
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = q + B.c * max(s.v食, 0.0) * u * ê + T.設定['kF'] * max(s.v食, 0.0) * (s.F - s.F.mean())
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            s.F[a] += T.設定['α'] * ((1.0 if 食べた else 0.0) - s.F[a]); return super().受ける(φ, a, q, e, 食べた, 我慢)
T.設定['kF'] = 3.0
def 一生(s, 層, 欠乏, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = 二層 if 層 else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def one(job):
    s, 層, 欠 = job; T.設定['kF'] = 3.0; o = 一生(s, 層, 欠); return (s, 層, 欠, M.P養(o, 7500, 7700), None if 欠 else B.区(o, 7000, 7500)[2])
腕 = [(層, 欠) for 層 in [False, True] for 欠 in [False, True]]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(19999, l, e, 7600)['sha256'] for l, e in 腕]; print('4腕が違う:', len(set(x)) == 4, ' 一層×欠乏＝S64:', 一生(19999, False, True)['sha256'] == M.一生(19999, '欠乏')['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(19800, 19830) if 段 == '本' else range(19900, 19930)
    with Pool(8) as p: r = p.map(one, [(s, l, e) for l, e in 腕 for s in S])
    d = {(s, l, e): (p_, a) for s, l, e, p_, a in r}
    増 = lambda s, l: d[(s, l, True)][0] - d[(s, l, False)][0]
    res = dict(H1_二層で戻って増える=int(sum(増(s, True) > 0 for s in S)), H2_増えが二層で大きい=int(sum(増(s, True) > 増(s, False) for s in S)), H3_普段を壊さない=int(sum(d[(s, True, False)][1] >= 0.9 * d[(s, False, False)][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {('二層' if l else '一層'): dict(増え=round(float(np.median([増(s, l) for s in S])), 3), P養_なし=round(float(np.median([d[(s, l, False)][0] for s in S])), 3), 見られ分け=round(float(np.median([d[(s, l, False)][1] for s in S])), 3)) for l in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
