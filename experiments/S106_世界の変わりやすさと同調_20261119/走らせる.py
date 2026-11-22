import sys, json, numpy as np
sys.path.insert(0, '../S106_世界の変わりやすさと同調_20261119')
from multiprocessing import Pool
from 共通 import H, B, W, N, K, L
kM = 5.0
def 一生(s, 間, 寿命=60000, 中立=False):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = H.写す; H.設定['kM'] = kM
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, 当たり固定=(間 == '固定'), 替わる間隔=1000 if 間 == '固定' else 間,
                       代替わり=2000, 代替わり間隔=250, 継ぐ=set(range(4)), 突然=0.1, 中立=中立)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8; H.設定['kM'] = 0.0
def one(job):
    s, 間 = job; o = 一生(s, 間); 列 = o['多数列']
    return (s, str(間), float(np.mean([n for t, n in 列 if t >= 10000])), float(o['食列'][10000:].mean()))
腕 = ['固定', 4000, 1000, 250]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 25199
        R104 = L('S104R', '../S104_同調は増えるか_20261119/走らせる.py')
        print('間隔1000 は S104 流行りと同じ sha:', 一生(s, 1000, 寿命=4000)['sha256'] == R104.一生(s, '流行り', 4, 寿命=4000)['sha256'])
        print('固定 は S104 固定と同じ sha:', 一生(s, '固定', 寿命=4000)['sha256'] == R104.一生(s, '固定', 4, 寿命=4000)['sha256'])
        o = 一生(s, 250, 寿命=4000); A = np.array(o['当たり']); print('間隔250 の当たりの数:', len(A), '（16+1 なら○）  隣が違う:', bool((A[1:] != A[:-1]).all()))
        y = [一生(s, 間, 寿命=9000)['sha256'] for 間 in 腕]; print('4腕が違う（9000手。4000手では固定と4000が同じ当たりのまま）:', len(set(y)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(25000, 25030) if 段 == '本' else range(25100, 25130)
    with Pool(8) as p: r = p.map(one, [(s, 間) for 間 in 腕 for s in S])
    d = {(s, 間): v for s, 間, *v in r}
    res = {'H1_固定のほうが250より多い': int(sum(d[(s, '固定')][0] > d[(s, '250')][0] for s in S)), 'H2_4000のほうが250より多い': int(sum(d[(s, '4000')][0] > d[(s, '250')][0] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {str(間): dict(同調者=round(float(np.median([d[(s, str(間))][0] for s in S])), 2), 食べ=round(float(np.median([d[(s, str(間))][1] for s in S])), 4)) for 間 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
