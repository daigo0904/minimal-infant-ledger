import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
T = L('S76R', '../S76_まねして学ぶ_20261119/走らせる.py')
B, W = T.B, T.W
N = L('S78世界', '../S78_お手本の子_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 見える, 寿命=8000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=見える, お手本=True)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数(o):
    A, 相, 当 = o['行動列'], o['相手列'], o['当たり']
    乗 = float(np.mean([(A[c:c + 500, 1:] == 当[c // 1000]).mean() for c in range(2000, 8000, 1000)]))
    n = m = 0
    for i in range(1, 8):
        t = np.arange(1, len(A)); sel = 相[t, i] == 1; t = t[sel]   # お手本（赤ちゃん0＝相手番号1）が見ている
        n += len(t); m += int((A[t, i] == A[t - 1, 0]).sum())
    return 乗, m / max(n, 1)
def one(job):
    s, v = job; o = 一生(s, v); return (s, v) + 数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(19199, True, 3000); A, 食, 当 = o['行動列'], o['食列'], o['当たり']
        print('赤ちゃん0 の手が当たりと一致:', bool((A[:, 0] == np.array(当)[np.arange(3000) // 1000]).all()), ' 赤ちゃん0 の食べた割合:', round(float(食[:, 0].mean()), 3), ' 他:', round(float(食[:, 1:].mean()), 3))
        print('見える≠見えない:', o['sha256'] != 一生(19199, False, 3000)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(19000, 19030) if 段 == '本' else range(19100, 19130)
    with Pool(8) as p: r = p.map(one, [(s, v) for v in [False, True] for s in S])
    d = {(s, v): (a, b) for s, v, a, b in r}
    res = dict(H1_見えると乗り換えが速い=int(sum(d[(s, True)][0] > d[(s, False)][0] for s in S)), H2_お手本をまねる=int(sum(d[(s, True)][1] > d[(s, False)][1] for s in S)), H3_見えるで乗り換えが起きる=int(sum(d[(s, True)][0] > 0.25 for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {('見える' if v else '見えない'): dict(乗り換え=round(float(np.median([d[(s, v)][0] for s in S])), 3), お手本まね=round(float(np.median([d[(s, v)][1] for s in S])), 3)) for v in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
