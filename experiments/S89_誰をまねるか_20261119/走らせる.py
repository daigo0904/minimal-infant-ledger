import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W = H.B, H.W
N = L('S89世界', '../S89_誰をまねるか_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
K = 16
def 一生(s, 見える, 寿命=8000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=見える, お手本=True, でたらめ=True)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def 数(o):
    """赤ちゃん2〜7 が、見ている相手の直前の手を写す割合：相手＝お手本（番号1）／でたらめ（番号2）／他の子（番号>2）"""
    A, 相 = o['行動列'], o['相手列']; r = {1: [], 2: [], 3: []}
    for i in range(2, 8):
        t = np.arange(1, len(A)); k = 相[t, i]
        for key, m in [(1, k == 1), (2, k == 2), (3, k > 2)]:
            tt = t[m]; r[key].append(float((A[tt, i] == A[tt - 1, 相[tt, i] - 1]).mean()))
    return tuple(float(np.mean(r[x])) for x in (1, 2, 3))
def one(job):
    s, v = job; o = 一生(s, v); return (s, v) + 数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(21399, True, 2000); A, 当 = o['行動列'], np.array(o['当たり'])[np.arange(2000) // 1000]
        print('赤ちゃん0 当たり一致:', bool((A[:, 0] == 当).all()), ' 赤ちゃん1 当たり一致率:', round(float((A[:, 1] == 当).mean()), 3), ' 手の種類:', len(set(A.ravel().tolist())))
        print('見える≠見えない:', o['sha256'] != 一生(21399, False, 2000)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(21200, 21230) if 段 == '本' else range(21300, 21330)
    with Pool(8) as p: r = p.map(one, [(s, v) for v in [False, True] for s in S])
    d = {(s, v): (a, b, c) for s, v, a, b, c in r}
    res = dict(H1_信頼できるほうをまねる=int(sum(d[(s, True)][0] > d[(s, True)][1] for s in S)), H2_選び分けは食べたかが見えると大きい=int(sum(d[(s, True)][0] - d[(s, True)][1] > d[(s, False)][0] - d[(s, False)][1] for s in S)),
               参考_見えなくても信頼できるほうをまねる=int(sum(d[(s, False)][0] > d[(s, False)][1] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_信頼できるほうをまねる', 'H2_選び分けは食べたかが見えると大きい']}
    res['中央値'] = {('見える' if v else '見えない'): dict(お手本を写す=round(float(np.median([d[(s, v)][0] for s in S])), 3), でたらめを写す=round(float(np.median([d[(s, v)][1] for s in S])), 3), 他の子を写す=round(float(np.median([d[(s, v)][2] for s in S])), 3)) for v in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
