import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S78R', '../S78_お手本の子_20261119/走らせる.py')
B, W = P.B, P.W
N = L('S80世界', '../S80_まねが広がるか_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
腕 = {'1/7': (True, 1 / 7), '0.5': (True, 0.5), 'なし': (False, 1 / 7)}
def 一生(s, 名, 寿命=8000):
    手本, f = 腕[名]; W.学び率 = 0.05; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=手本, お手本の頻度=f)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数(o):
    A, 相, 当 = o['行動列'], o['相手列'], np.array(o['当たり']); 当t = 当[np.arange(len(A)) // 1000]
    vals = []
    for c in range(2000, 8000, 1000):
        sl = slice(c, c + 500); x = []
        for i in range(1, 8):
            m = 相[sl, i] > 1; x.append((A[sl, i][m] == 当t[sl][m]).mean())
        vals.append(np.mean(x))
    return float(np.mean(vals))
def one(job):
    s, 名 = job; o = 一生(s, 名); return (s, 名, 数(o))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = {}
        for 名 in 腕:
            o = 一生(19599, 名, 600); 相 = o['相手列']; x[名] = o['sha256']
            print(名, ' 赤ちゃん0 が見る手の割合（1〜7）:', round(float((相[:, 1:] == 1).mean()), 3))
        print('3腕が違う:', len(set(x.values())) == 3); sys.exit()
    段 = sys.argv[1]; S = range(19400, 19430) if 段 == '本' else range(19500, 19530)
    with Pool(8) as p: r = p.map(one, [(s, n) for n in 腕 for s in S])
    d = {(s, n): v for s, n, v in r}
    res = dict(H1_まねが広がる=int(sum(d[(s, '0.5')] > d[(s, 'なし')] for s in S)), H2_よく見るほど広がる=int(sum(d[(s, '0.5')] > d[(s, '1/7')] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値_お手本以外が見る時の当たり'] = {n: round(float(np.median([d[(s, n)] for s in S])), 3) for n in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
