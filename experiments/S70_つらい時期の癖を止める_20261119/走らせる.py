import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S68R', '../S68_欠乏の後に下げる力_20261119/走らせる.py')
B, W, N, M = R.B, R.W, R.N, R.M
止める = [False]; 写し = {}
class 止まる(R.記す):
    """手数 7000〜7500 の間だけ Q の学びを止める（W.学び率 を 0 にして super を呼ぶ）。他の学びはそのまま"""
    def __init__(s, *a): super().__init__(*a); s.手数 = 0
    def 選ぶ(s, φ):
        s.手数 += 1
        if s.手数 == 7001: 写し[(s.番, 7000)] = s.Q.copy()
        if s.手数 == 7501: 写し[(s.番, 7500)] = s.Q.copy()
        return super().選ぶ(φ)
    def 受ける(s, *a, **k):
        if 止める[0] and 7000 < s.手数 <= 7500:
            W.学び率 = 0.0
            try: return super().受ける(*a, **k)
            finally: W.学び率 = 0.01
        return super().受ける(*a, **k)
def 一生(s, 止, 欠乏, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; R.記録.clear(); R.一番[0] = R.一番を調べる(s); 止める[0] = 止; 写し.clear(); N.赤ちゃん = 止まる
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def one(job):
    s, 止, 欠 = job; o = 一生(s, 止, 欠)
    Rm = np.array([R.記録[i] for i in range(8)]).transpose(1, 0, 2); 相 = o['相手列']; m = 相[7500:7700] == 0
    return (s, 止, 欠, float(Rm[7500:7700][m][:, 0].mean()), M.P養(o, 7500, 7700))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(17599, True, True, 7600); q = dict(写し)
        print('止めると 7000→7500 で Q 一致:', all(np.allclose(q[(i, 7000)], q[(i, 7500)]) for i in range(8)))
        b = 一生(17599, False, True, 7600); q2 = dict(写し); print('止めないと Q が動く:', not all(np.allclose(q2[(i, 7000)], q2[(i, 7500)]) for i in range(8)))
        print('7000まで同じ:', bool((a['行動列'][:7000] == b['行動列'][:7000]).all()), ' 止めない＝S68:', b['sha256'] == R.一生(17599, True, True, 7600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(17400, 17430) if 段 == '本' else range(17500, 17530)
    with Pool(8) as p: r = p.map(one, [(s, t, e) for t in [False, True] for e in [False, True] for s in S])
    d = {(s, t, e): (q, p) for s, t, e, q, p in r}
    res = dict(H1_止めると戻って増える=int(sum(d[(s, True, True)][1] > d[(s, True, False)][1] for s in S)), H2_止めると癖が下げない=int(sum(d[(s, True, True)][0] >= d[(s, True, False)][0] for s in S)),
               参考_止めないで戻って増える=int(sum(d[(s, False, True)][1] > d[(s, False, False)][1] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_止めると戻って増える', 'H2_止めると癖が下げない']}
    res['中央値'] = {f'{"止める" if t else "止めない"}_{"欠乏" if e else "なし"}': dict(Q差=round(float(np.median([d[(s, t, e)][0] for s in S])), 4), P養=round(float(np.median([d[(s, t, e)][1] for s in S])), 3)) for t in [False, True] for e in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
