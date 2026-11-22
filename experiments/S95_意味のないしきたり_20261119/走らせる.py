import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W = H.B, H.W
N = L('S95世界', '../S95_意味のないしきたり_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
K = 16
def しきたりの手(s):
    世 = np.random.default_rng([s, 0]); 当 = int(np.random.default_rng([s, 7]).integers(K))
    return (当 + 5) % K   # 当たりとは違う手（食べ物は出ない）
def 一生(s, 型, 褒める, 寿命=6000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=False, 当たり固定=True, 新入り=4000, 仲間は褒めない=not 褒める,
                       しきたり=しきたりの手(s) if 型 == '決まった手' else 'でたらめ')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def one(job):
    s, 型, 褒 = job; o = 一生(s, 型, 褒); A = o['行動列']; x = しきたりの手(s)
    return (s, 型, 褒, float((A[4500:6000, 7] == x).mean()), float((A[4500:6000, 7] == o['当たり'][0]).mean()))
腕 = [(型, 褒) for 型 in ['でたらめ', '決まった手'] for 褒 in [True, False]]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(22599, '決まった手', True, 4300); x = しきたりの手(22599); A = o['行動列']
        print('しきたりの手:', x, ' 当たり:', o['当たり'][0], ' 4000〜 仲間0〜6 が全部しきたりの手:', bool((A[4000:, :7] == x).all()), ' 4000前は違う:', bool((A[3000:4000, :7] != x).any()), ' しきたりの手で食べた割合:', round(float(o['食列'][4000:, :7].mean()), 3))
        y = [一生(22599, 型, 褒, 4300)['sha256'] for 型, 褒 in 腕]; print('4腕が違う:', len(set(y)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(22400, 22430) if 段 == '本' else range(22500, 22530)
    with Pool(8) as p: r = p.map(one, [(s, 型, 褒) for 型, 褒 in 腕 for s in S])
    d = {(s, 型, 褒): (a, b) for s, 型, 褒, a, b in r}
    効 = lambda s, 褒: d[(s, '決まった手', 褒)][0] - d[(s, 'でたらめ', 褒)][0]
    res = dict(H1_しきたりが新入りに伝わる=int(sum(効(s, True) > 0 for s in S)), H2_褒めないと伝わらない=int(sum(効(s, False) < 効(s, True) for s in S)), 参考_褒めなくても伝わる=int(sum(効(s, False) > 0 for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_しきたりが新入りに伝わる', 'H2_褒めないと伝わらない']}
    res['中央値'] = {f'{型}_{"褒める" if 褒 else "褒めない"}': dict(新入りのしきたりの手=round(float(np.median([d[(s, 型, 褒)][0] for s in S])), 3), 新入りの当たり=round(float(np.median([d[(s, 型, 褒)][1] for s in S])), 3)) for 型, 褒 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
