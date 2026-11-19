import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W, N = H.B, H.W, H.N
好み = {4: [-0.8, -0.2, 0.3, 0.9], 8: [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 4, 16: [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12}
def 一生(s, 手の数, 手本, 寿命=8000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = 手の数; W.行動数 = 手の数; N.養育者の好み = 好み[手の数]; W.見た目次元 = 8 + 手の数 + 1; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=手本, お手本の頻度=0.5)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = 好み[4]; W.見た目次元 = 8
腕 = [(k, 手) for k in [4, 16] for 手 in [False, True]]
def one(job):
    s, k, 手 = job; o = 一生(s, k, 手); return (s, k, 手) + H.数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(21199, k, 手, 600)['sha256'] for k, 手 in 腕]; print('4腕が違う:', len(set(x)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(21000, 21030) if 段 == '本' else range(21100, 21130)
    with Pool(8) as p: r = p.map(one, [(s, k, 手) for k, 手 in 腕 for s in S])
    d = {(s, k, 手): (a, b, c) for s, k, 手, a, b, c in r}
    効 = lambda s, k, j: d[(s, k, True)][j] - d[(s, k, False)][j]
    res = dict(H1_まねの知識は手16で大きい=int(sum(効(s, 16, 1) > 効(s, 4, 1) for s in S)), H2_お手本の乗り換えの得は手16で大きい=int(sum(効(s, 16, 0) > 効(s, 4, 0) for s in S)),
               参考_手4でまねが知識に=int(sum(効(s, 4, 1) > 0 for s in S)), 参考_手16でまねが知識に=int(sum(効(s, 16, 1) > 0 for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_まねの知識は手16で大きい', 'H2_お手本の乗り換えの得は手16で大きい']}
    res['中央値'] = {f'手{k}_{"お手本あり" if 手 else "なし"}': dict(乗り換え=round(float(np.median([d[(s, k, 手)][0] for s in S])), 3), 他が見る時=round(float(np.median([d[(s, k, 手)][1] for s in S])), 3)) for k, 手 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
