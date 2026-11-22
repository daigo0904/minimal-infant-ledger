import sys, json, numpy as np
sys.path.insert(0, '../S104_同調は増えるか_20261119')
from multiprocessing import Pool
from 共通 import H, B, W, N, K, L
kM = 5.0
def 一生(s, 世界, m, 寿命=20000, 間隔=250, 中立=False, 突然=0.1):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = H.写す; H.設定['kM'] = kM
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, 当たり固定=(世界 == '固定'), 代替わり=2000, 代替わり間隔=間隔, 継ぐ=set(range(m)), 突然=突然, 中立=中立)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8; H.設定['kM'] = 0.0
def one(job):
    s, 世界, m = job; o = 一生(s, 世界, 4, 中立=(m == '中立')); 列 = o['多数列']
    後 = [n for t, n in 列 if t >= 10000]
    return (s, 世界, m, float(np.mean(後)), [n for t, n in 列][::8], float(o['食列'][15000:].mean()))
腕 = [(世界, m) for 世界 in ['固定', '流行り'] for m in ['選び', '中立']]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 24399; o = 一生(s, '固定', 4, 寿命=3000, 間隔=100); 列 = o['多数列']
        print('代替わりの回数:', len(列), '（2000〜3000 を100ごと＝10回なら○）', ' 同調者の数の並び:', [n for t, n in 列])
        print('取り分=0 なら同調者は生まれない（m=0）:', (lambda L: len(L) == 10 and all(n == 0 for t, n in L))(一生(s, '固定', 0, 寿命=3000, 間隔=100, 突然=0.0)['多数列']), ' 取り分=1（m=8）なら全員のまま:', (lambda L: len(L) == 10 and all(n == 8 for t, n in L))(一生(s, '固定', 8, 寿命=3000, 間隔=100, 突然=0.0)['多数列']))
        R103 = L('S103R', '../S103_同調者の割合_20261119/頭.py')
        y = [一生(s, w, 4, 中立=(m == '中立'))['sha256'] for w, m in 腕]; print('4腕が違う:', len(set(y)) == 4)
        for w in ['固定', '流行り']: print(w, [(m, [round(v, 3) if isinstance(v, float) else v for v in one((s, w, m))[3:]]) for m in ['選び', '中立']])
        sys.exit()
    段 = sys.argv[1]; S = range(24400, 24430) if 段 == '本' else range(24500, 24530)
    with Pool(8) as p: r = p.map(one, [(s, w, m) for w, m in 腕 for s in S])
    d = {(s, w, m): v for s, w, m, *v in r}
    res = {}
    for w in ['固定', '流行り']:
        res[f'H_{w}_選びで{"増える" if w == "固定" else "減る"}'] = int(sum((d[(s, w, '選び')][0] > d[(s, w, '中立')][0]) if w == '固定' else (d[(s, w, '選び')][0] < d[(s, w, '中立')][0]) for s in S))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{w}_{m}': dict(終わりの同調者=round(float(np.median([d[(s, w, m)][0] for s in S])), 2), 全員になった世界=int(sum(d[(s, w, m)][0] >= 7.5 for s in S)), いなくなった世界=int(sum(d[(s, w, m)][0] <= 0.5 for s in S)), 食べ=round(float(np.median([d[(s, w, m)][2] for s in S])), 4)) for w, m in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
