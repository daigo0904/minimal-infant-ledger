import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W = H.B, H.W
N = L('S90世界', '../S90_信頼の入れ替わり_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
K = 16
def 一生(s, 替える, 寿命=8000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=True, でたらめ=True, 入れ替え=4000 if 替える else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def 数(o, a=7000, b=8000):
    """赤ちゃん2〜7 が、見ている相手の直前の手を写す割合：相手＝お手本（番号1）／でたらめ（番号2）／他の子（番号>2）"""
    A, 相 = o['行動列'], o['相手列']; r = {1: [], 2: [], 3: []}
    for i in range(2, 8):
        t = np.arange(a, b); k = 相[t, i]
        for key, m in [(1, k == 1), (2, k == 2), (3, k > 2)]:
            tt = t[m]; r[key].append(float((A[tt, i] == A[tt - 1, 相[tt, i] - 1]).mean()))
    return tuple(float(np.mean(r[x])) for x in (1, 2, 3))
def one(job):
    s, v = job; o = 一生(s, v); return (s, v) + 数(o, 3000, 4000) + 数(o, 7000, 8000)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(21599, True, 5000); A, 当 = o['行動列'], np.array(o['当たり'])[np.arange(5000) // 1000]
        print('〜4000 赤ちゃん0 当たり一致:', bool((A[:4000, 0] == 当[:4000]).all()), ' 4000〜 赤ちゃん1 当たり一致:', bool((A[4000:, 1] == 当[4000:]).all()), ' 4000〜 赤ちゃん0 一致率:', round(float((A[4000:, 0] == 当[4000:]).mean()), 3))
        b = 一生(21599, False, 5000); print('4000まで同じ:', bool((A[:4000] == b['行動列'][:4000]).all()), ' 4000〜で違う:', bool((A[4000:] != b['行動列'][4000:]).any())); sys.exit()
    段 = sys.argv[1]; S = range(21400, 21430) if 段 == '本' else range(21500, 21530)
    with Pool(8) as p: r = p.map(one, [(s, v) for v in [False, True] for s in S])
    d = {(s, v): x for s, v, *x in r}
    # x = [前: 0を写す, 1を写す, 他, 後: 0を写す, 1を写す, 他]
    res = dict(H1_入れ替え後は新しいお手本を多く写す=int(sum(d[(s, True)][4] > d[(s, True)][3] for s in S)), H2_入れ替えで写す相手が逆転する=int(sum((d[(s, True)][4] - d[(s, True)][3]) - (d[(s, False)][4] - d[(s, False)][3]) > 0 for s in S)),
               参考_入れ替え前は赤ちゃん0を多く写す=int(sum(d[(s, True)][0] > d[(s, True)][1] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_入れ替え後は新しいお手本を多く写す', 'H2_入れ替えで写す相手が逆転する']}
    名 = ['前_0を写す', '前_1を写す', '前_他', '後_0を写す', '後_1を写す', '後_他']
    res['中央値'] = {('替える' if v else '替えない'): {名[k]: round(float(np.median([d[(s, v)][k] for s in S])), 3) for k in range(6)} for v in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
