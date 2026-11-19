import sys, json, numpy as np
from multiprocessing import Pool
import 頭 as H
H.記憶.設定.update(kD=10.0, 容量=100)
腕 = [(層, 手) for 層 in [False, True] for 手 in [False, True]]
def one(job):
    s, 層, 手 = job; H.記憶.設定.update(kD=10.0, 容量=100); o = H.一生(s, 層, 手本=手); return (s, 層, 手) + H.数(o)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [H.一生(20199, 層, 手, 600)['sha256'] for 層, 手 in 腕]; print('4腕が違う:', len(set(x)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(20000, 20030) if 段 == '本' else range(20100, 20130)
    with Pool(8) as p: r = p.map(one, [(s, 層, 手) for 層, 手 in 腕 for s in S])
    d = {(s, 層, 手): (a, b, c) for s, 層, 手, a, b, c in r}
    効 = lambda s, 層: d[(s, 層, True)][1] - d[(s, 層, False)][1]
    res = dict(H1_記憶でまねが知識になる=int(sum(効(s, True) > 0 for s in S)), H2_記憶のほうがお手本の効きが大きい=int(sum(効(s, True) > 効(s, False) for s in S)),
               H3_お手本ありで記憶が乗り換え速い=int(sum(d[(s, True, True)][0] > d[(s, False, True)][0] for s in S)), 参考_お手本が見る時の当たり_記憶>一層=int(sum(d[(s, True, True)][2] > d[(s, False, True)][2] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_記憶でまねが知識になる', 'H2_記憶のほうがお手本の効きが大きい', 'H3_お手本ありで記憶が乗り換え速い']}
    res['中央値'] = {f'{"記憶" if 層 else "一層"}_{"お手本あり" if 手 else "なし"}': dict(乗り換え=round(float(np.median([d[(s, 層, 手)][0] for s in S])), 3), 他が見る時=round(float(np.median([d[(s, 層, 手)][1] for s in S])), 3), お手本が見る時=round(float(np.median([d[(s, 層, 手)][2] for s in S])), 3)) for 層, 手 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
