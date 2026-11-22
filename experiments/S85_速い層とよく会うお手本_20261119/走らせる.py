import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W, N = H.B, H.W, H.N
H.設定.update(kF=3.0, α=0.1)
def 一生(s, 層, 手本, 寿命=8000):
    H.設定.update(kF=3.0, α=0.1); W.学び率 = 0.05; B.v時定数 = 5000.0; W.見た目次元 = 13; N.赤ちゃん = H.二層 if 層 else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=手本, お手本の頻度=0.5)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
腕 = [(層, 手) for 層 in [False, True] for 手 in [False, True]]
def one(job):
    s, 層, 手 = job; o = 一生(s, 層, 手); return (s, 層, 手) + H.数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(20599, True, True, 600); print('赤ちゃん0 が見る手の割合:', round(float((o['相手列'][:, 1:] == 1).mean()), 3))
        x = [一生(20599, 層, 手, 600)['sha256'] for 層, 手 in 腕]; print('4腕が違う:', len(set(x)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(20400, 20430) if 段 == '本' else range(20500, 20530)
    with Pool(8) as p: r = p.map(one, [(s, 層, 手) for 層, 手 in 腕 for s in S])
    d = {(s, 層, 手): (a, b, c) for s, 層, 手, a, b, c in r}
    効 = lambda s, 層: d[(s, 層, True)][1] - d[(s, 層, False)][1]
    res = dict(H1_速い層でまねが知識になる=int(sum(効(s, True) > 0 for s in S)), H2_速い層のほうがお手本の効きが大きい=int(sum(効(s, True) > 効(s, False) for s in S)), 参考_一層でまねが知識になる=int(sum(効(s, False) > 0 for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_速い層でまねが知識になる', 'H2_速い層のほうがお手本の効きが大きい']}
    res['中央値'] = {f'{"速い層" if 層 else "一層"}_{"お手本あり" if 手 else "なし"}': dict(乗り換え=round(float(np.median([d[(s, 層, 手)][0] for s in S])), 3), 他が見る時=round(float(np.median([d[(s, 層, 手)][1] for s in S])), 3), お手本が見る時=round(float(np.median([d[(s, 層, 手)][2] for s in S])), 3)) for 層, 手 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
