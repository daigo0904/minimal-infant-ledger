import sys, json, numpy as np, importlib.util
sys.path.insert(0, '../S106_世界の変わりやすさと同調_20261119')
from multiprocessing import Pool
from 共通 import H, B, W, N, K, L, しきたりの手
kM = 5.0
def 一生(s, 型, 中立, 寿命=60000):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = H.写す; H.設定['kM'] = kM
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, 当たり固定=True, しきたり=しきたりの手(s) if 型 == '決まった手' else 'でたらめ', しきたり始め=1000,
                       代替わり=2000, 代替わり間隔=250, 継ぐ=set(range(8)), 突然=0.1, 中立=中立)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8; H.設定['kM'] = 0.0
def one(job):
    s, 型, 中 = job; o = 一生(s, 型, 中); A = o['行動列']; x = しきたりの手(s); 列 = o['多数列']
    return (s, 型, 中, float(np.mean([n for t, n in 列 if t >= 10000])), float((A[4000:10000] == x).mean()), float((A[10000:] == x).mean()), float((A[50000:] == x).mean()), float(o['食列'][10000:].mean()))
腕 = [(型, 中) for 中 in [False, True] for 型 in ['でたらめ', '決まった手']]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 25399; x = しきたりの手(s); o = 一生(s, '決まった手', False, 寿命=6000); A = o['行動列']
        print('1000〜2000 で0〜6 全部しきたり:', bool((A[1000:2000, :7] == x).all()), ' 3500〜 で6 は全部しきたりでない:', bool((A[3500:, 6] != x).any()), ' 代替わり回数:', len(o['多数列']), '（16なら○）')
        print('4000〜6000 しきたり:', round(float((A[4000:6000] == x).mean()), 3), ' 同調者の数の並び:', [n for t, n in o['多数列']])
        y = [一生(s, 型, 中, 寿命=15000)['sha256'] for 型, 中 in 腕]; print('4腕が違う:', len(set(y)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(25200, 25230) if 段 == '本' else range(25300, 25330)
    with Pool(8) as p: r = p.map(one, [(s, 型, 中) for 型, 中 in 腕 for s in S])
    d = {(s, 型, 中): v for s, 型, 中, *v in r}
    効 = lambda s, 中, k: d[(s, '決まった手', 中)][k] - d[(s, 'でたらめ', 中)][k]
    res = {'H1_しきたりがあると選びで同調者が減る': int(sum(d[(s, '決まった手', False)][0] < d[(s, 'でたらめ', False)][0] for s in S)),
           'H2_しきたりは中立のほうが長く残る': int(sum(効(s, True, 2) > 効(s, False, 2) for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{"中立" if 中 else "選び"}_{型}': dict(同調者=round(float(np.median([d[(s, 型, 中)][0] for s in S])), 2), しきたり_4千から1万=round(float(np.median([d[(s, 型, 中)][1] for s in S])), 3), しきたり_1万から=round(float(np.median([d[(s, 型, 中)][2] for s in S])), 3), しきたり_5万から=round(float(np.median([d[(s, 型, 中)][3] for s in S])), 3), 食べ=round(float(np.median([d[(s, 型, 中)][4] for s in S])), 4)) for 型, 中 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
