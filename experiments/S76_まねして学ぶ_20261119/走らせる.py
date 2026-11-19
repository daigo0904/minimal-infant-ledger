import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S50R', '../S50_相手の直前の手が見える_20261118/走らせる.py')
B, W = R.B, R.W
N = L('S76世界', '../S76_まねして学ぶ_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 見える, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=見える)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数(o):
    A, 相, 食, 当 = o['行動列'], o['相手列'], o['食列'], o['当たり']
    立ち上がり = float(np.mean([(A[c:c + 200] == 当[c // 1000]).mean() for c in range(2000, 8000, 1000)]))
    n = m = 0
    for i in range(8):
        t = np.arange(1, len(A)); k = 相[t, i]; sel = k > 0; t, k = t[sel], k[sel]
        c = 食[t - 1, k - 1] & (A[t - 1, k - 1] == np.array(当)[t // 1000])
        n += int(c.sum()); m += int((c & (A[t, i] == A[t - 1, k - 1])).sum())
    return 立ち上がり, m / max(n, 1)
def one(job):
    s, v = job; o = 一生(s, v); return (s, v) + 数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(18799, True, 3000); 当 = o['当たり']; A, 食 = o['行動列'], o['食列']
        print('当たり:', 当[:4], ' 当たりの手の時の食べた割合:', round(float(食[A == np.array(当)[np.arange(3000) // 1000][:, None]].mean()), 3), ' 他の手:', round(float(食[A != np.array(当)[np.arange(3000) // 1000][:, None]].mean()), 3))
        W.見た目次元 = 13; c = B.換算(18799, 0, '獲得型'); print('感覚の W:', c.感覚.W.shape); W.見た目次元 = 8
        print('見える≠見えない:', o['sha256'] != 一生(18799, False, 3000)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(18600, 18630) if 段 == '本' else range(18700, 18730)
    with Pool(8) as p: r = p.map(one, [(s, v) for v in [False, True] for s in S])
    d = {(s, v): (a, b) for s, v, a, b in r}
    res = dict(H1_切り替えで早く乗り換える=int(sum(d[(s, True)][0] > d[(s, False)][0] for s in S)), H2_食べた子をまねる=int(sum(d[(s, True)][1] > d[(s, False)][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {('見える' if v else '見えない'): dict(立ち上がり=round(float(np.median([d[(s, v)][0] for s in S])), 3), まね=round(float(np.median([d[(s, v)][1] for s in S])), 3)) for v in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
