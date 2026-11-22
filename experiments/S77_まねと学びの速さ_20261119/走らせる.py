import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
T = L('S76R', '../S76_まねして学ぶ_20261119/走らせる.py')
B, W, N = T.B, T.W, T.N
def 一生(s, 見える, lr, 寿命=8000):
    W.学び率 = lr; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=見える)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 乗り換え(o):
    A, 当 = o['行動列'], o['当たり']; return float(np.mean([(A[c:c + 500] == 当[c // 1000]).mean() for c in range(2000, 8000, 1000)]))
def one(job):
    s, v, lr = job; o = 一生(s, v, lr); return (s, v, lr, 乗り換え(o))
腕 = [(v, lr) for v in [False, True] for lr in [0.01, 0.05]]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(18999, v, lr, 600)['sha256'] for v, lr in 腕]; print('4腕が違う:', len(set(x)) == 4, ' 0.01見える＝S76:', 一生(18999, True, 0.01, 600)['sha256'] == T.一生(18999, True, 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(18800, 18830) if 段 == '本' else range(18900, 18930)
    with Pool(8) as p: r = p.map(one, [(s, v, lr) for v, lr in 腕 for s in S])
    d = {(s, v, lr): x for s, v, lr, x in r}
    res = dict(H1_学び率0_01で見えると速い=int(sum(d[(s, True, 0.01)] > d[(s, False, 0.01)] for s in S)), H2_学び率0_05で見えると速い=int(sum(d[(s, True, 0.05)] > d[(s, False, 0.05)] for s in S)),
               H3_0_05で乗り換えが起きる=int(sum(d[(s, False, 0.05)] > 0.25 for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{"見える" if v else "見えない"}_{lr}': round(float(np.median([d[(s, v, lr)] for s in S])), 3) for v, lr in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
