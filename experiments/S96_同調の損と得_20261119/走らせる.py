import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S95R', '../S95_意味のないしきたり_20261119/走らせる.py')
B, W, N, K = P.B, P.W, P.N, P.K
def 当たりの手(s): return int(np.random.default_rng([s, 7]).integers(K))
def 一生(s, 型, 褒める, 寿命=6000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=False, 当たり固定=True, 新入り=4000, 仲間は褒めない=not 褒める,
                       しきたり=当たりの手(s) if 型 == '当たり' else 'でたらめ')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def one(job):
    s, 型, 褒 = job; o = 一生(s, 型, 褒); A = o['行動列']
    return (s, 型, 褒, float((A[4500:6000, 7] == o['当たり'][0]).mean()), float(o['食列'][4500:6000, 7].mean()))
腕 = [(型, 褒) for 型 in ['でたらめ', '当たり'] for 褒 in [True, False]]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(22799, '当たり', True, 4300); A = o['行動列']
        print('4000〜 仲間が全部当たり:', bool((A[4000:, :7] == o['当たり'][0]).all()), ' 当たりの手の確認:', 当たりの手(22799) == o['当たり'][0])
        y = [一生(22799, 型, 褒, 4300)['sha256'] for 型, 褒 in 腕]; print('4腕が違う:', len(set(y)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(22600, 22630) if 段 == '本' else range(22700, 22730)
    with Pool(8) as p: r = p.map(one, [(s, 型, 褒) for 型, 褒 in 腕 for s in S])
    d = {(s, 型, 褒): (a, f) for s, 型, 褒, a, f in r}
    res = dict(H1_多数がでたらめだと承認は損=int(sum(d[(s, 'でたらめ', True)][0] < d[(s, 'でたらめ', False)][0] for s in S)), H2_多数が当たりだと承認は得=int(sum(d[(s, '当たり', True)][0] > d[(s, '当たり', False)][0] for s in S)),
               参考_食べた割合_でたらめで損=int(sum(d[(s, 'でたらめ', True)][1] < d[(s, 'でたらめ', False)][1] for s in S)), 参考_食べた割合_当たりで得=int(sum(d[(s, '当たり', True)][1] > d[(s, '当たり', False)][1] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_多数がでたらめだと承認は損', 'H2_多数が当たりだと承認は得']}
    res['中央値'] = {f'{型}_{"褒める" if 褒 else "褒めない"}': dict(新入りの当たり=round(float(np.median([d[(s, 型, 褒)][0] for s in S])), 3), 食べた=round(float(np.median([d[(s, 型, 褒)][1] for s in S])), 4)) for 型, 褒 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
