import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W = H.B, H.W
N = L('S92世界', '../S92_文化の伝わり_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
K = 16
def 一生(s, 手本, 寿命=6000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=True, お手本まで=4000 if 手本 else 0, 当たり固定=True, 新入り=4000)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def 数(o):
    A, 当 = o['行動列'], o['当たり'][0]
    return float((A[4000:4500, 7] == 当).mean()), float((A[4000:5000, 7] == 当).mean()), float((A[3500:4000, 2:7] == 当).mean()), float((A[4000:5000, 2:7] == 当).mean())
def one(job):
    s, 手 = job; o = 一生(s, 手); return (s, 手) + 数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(21999, True, 4600); b = 一生(21999, False, 4600); 当 = a['当たり'][0]
        print('当たり固定:', len(set(a['当たり'])) == 1, ' 赤ちゃん0 〜4000 当たり一致:', bool((a['行動列'][:4000, 0] == 当).all()), ' 4000〜 一致率:', round(float((a['行動列'][4000:, 0] == 当).mean()), 3), ' お手本なしの赤ちゃん0 一致率:', round(float((b['行動列'][:, 0] == 当).mean()), 3))
        print('赤ちゃん7 の当たり率 3500〜4000 / 4000〜4100（新入り直後）:', round(float((a['行動列'][3500:4000, 7] == 当).mean()), 3), round(float((a['行動列'][4000:4100, 7] == 当).mean()), 3), ' あり≠なし:', a['sha256'] != b['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(21800, 21830) if 段 == '本' else range(21900, 21930)
    with Pool(8) as p: r = p.map(one, [(s, t) for t in [False, True] for s in S])
    d = {(s, t): x for s, t, *x in r}
    res = dict(H1_新入りが早く当たりを覚える=int(sum(d[(s, True)][0] > d[(s, False)][0] for s in S)), H2_新入りの最初の1000手=int(sum(d[(s, True)][1] > d[(s, False)][1] for s in S)),
               参考_仲間がお手本から覚えていた=int(sum(d[(s, True)][2] > d[(s, False)][2] for s in S)), 参考_お手本が去った後も仲間に残る=int(sum(d[(s, True)][3] > d[(s, False)][3] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_新入りが早く当たりを覚える', 'H2_新入りの最初の1000手']}
    名 = ['新入り_最初500', '新入り_最初1000', '仲間_3500〜4000', '仲間_4000〜5000']
    res['中央値'] = {('お手本あり' if t else 'なし'): {名[k]: round(float(np.median([d[(s, t)][k] for s in S])), 3) for k in range(4)} for t in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
