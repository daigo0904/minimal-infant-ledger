import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S81頭', '../S81_速い層でまねが知識になるか_20261119/頭.py')
B, W = H.B, H.W
N = L('S94世界', '../S94_見てか褒められてか_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
K = 16
条件 = {'両方': (False, False), '見せない': (True, False), '褒めない': (False, True)}
def 一生(s, 知る, 条, 寿命=6000):
    見せ, 褒め = 条件[条]
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=False, 当たり固定=True, 新入り=4000, 全員新入り=not 知る, 手を見せない=見せ, 仲間は褒めない=褒め)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def one(job):
    s, 知, 条 = job; o = 一生(s, 知, 条); A, 当 = o['行動列'], o['当たり'][0]
    return (s, 知, 条, float((A[4000:4500, 7] == 当).mean()), float((A[3500:4000, 0:7] == 当).mean()))
腕 = [(知, 条) for 条 in 条件 for 知 in [False, True]]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(22399, 知, 条, 600)['sha256'] for 知, 条 in 腕]; print('両方≠見せない≠褒めない（知る仲間・600手）:', len({一生(22399, True, c, 600)['sha256'] for c in 条件}) == 3)
        a = 一生(22399, True, '両方', 600); b = 一生(22399, True, '両方', 600)
        print('同じ設定で同じ一生（再現）:', a['sha256'] == b['sha256'], ' 両方＝S93 の知る仲間:', a['sha256'] == L('S93R', '../S93_知っている仲間の中に生まれる_20261119/走らせる.py').一生(22399, True, 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(22200, 22230) if 段 == '本' else range(22300, 22330)
    with Pool(8) as p: r = p.map(one, [(s, 知, 条) for 知, 条 in 腕 for s in S])
    d = {(s, 知, 条): (a, b) for s, 知, 条, a, b in r}
    効 = lambda s, 条: d[(s, True, 条)][0] - d[(s, False, 条)][0]
    res = dict(H1_手が見えないと伝わりが減る=int(sum(効(s, '見せない') < 効(s, '両方') for s in S)), H2_褒めないと伝わりが減る=int(sum(効(s, '褒めない') < 効(s, '両方') for s in S)),
               参考_両方で伝わる=int(sum(効(s, '両方') > 0 for s in S)), 参考_見せないでも伝わる=int(sum(効(s, '見せない') > 0 for s in S)), 参考_褒めないでも伝わる=int(sum(効(s, '褒めない') > 0 for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_手が見えないと伝わりが減る', 'H2_褒めないと伝わりが減る']}
    res['中央値'] = {条: dict(新入り_知る=round(float(np.median([d[(s, True, 条)][0] for s in S])), 3), 新入り_全員=round(float(np.median([d[(s, False, 条)][0] for s in S])), 3), 伝わり=round(float(np.median([効(s, 条) for s in S])), 3), 仲間の当たり=round(float(np.median([d[(s, True, 条)][1] for s in S])), 3)) for 条 in 条件}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
