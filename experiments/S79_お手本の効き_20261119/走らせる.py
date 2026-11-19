import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S78R', '../S78_お手本の子_20261119/走らせる.py')
B, W, N = P.B, P.W, P.N
def 一生(s, 手本, 寿命=8000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=手本)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数(o):
    A, 相, 当 = o['行動列'], o['相手列'], np.array(o['当たり'])
    乗 = float(np.mean([(A[c:c + 500, 1:] == 当[c // 1000]).mean() for c in range(2000, 8000, 1000)]))
    当t = 当[np.arange(len(A)) // 1000]
    a0 = []; ao = []
    for i in range(1, 8):
        a0.append((A[相[:, i] == 1, i] == 当t[相[:, i] == 1]).mean()); m = 相[:, i] > 1; ao.append((A[m, i] == 当t[m]).mean())
    return 乗, float(np.mean(a0)), float(np.mean(ao))
def one(job):
    s, 手 = job; o = 一生(s, 手); return (s, 手) + 数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(19399, True, 2000); b = 一生(19399, False, 2000); 当 = np.array(b['当たり'])[np.arange(2000) // 1000]
        print('あり≠なし:', a['sha256'] != b['sha256'], ' なしで赤ちゃん0 が当たりと一致する割合:', round(float((b['行動列'][:, 0] == 当).mean()), 3), ' あり＝S78 見える:', a['sha256'] == P.一生(19399, True, 2000)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(19200, 19230) if 段 == '本' else range(19300, 19330)
    with Pool(8) as p: r = p.map(one, [(s, t) for t in [False, True] for s in S])
    d = {(s, t): (a, b, c) for s, t, a, b, c in r}
    res = dict(H1_お手本で乗り換えが速い=int(sum(d[(s, True)][0] > d[(s, False)][0] for s in S)), H2_お手本が見ている時だけ当たりが増える=int(sum(d[(s, True)][1] > d[(s, True)][2] for s in S)),
               参考_お手本なしで同じ比べ=int(sum(d[(s, False)][1] > d[(s, False)][2] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_お手本で乗り換えが速い', 'H2_お手本が見ている時だけ当たりが増える']}
    res['中央値'] = {('あり' if t else 'なし'): dict(乗り換え=round(float(np.median([d[(s, t)][0] for s in S])), 3), 当たり_赤ちゃん0が見る=round(float(np.median([d[(s, t)][1] for s in S])), 3), 当たり_他が見る=round(float(np.median([d[(s, t)][2] for s in S])), 3)) for t in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
