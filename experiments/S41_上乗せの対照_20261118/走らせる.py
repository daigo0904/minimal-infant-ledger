import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
def 一生(s, 頭, 世界, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.赤ちゃん = B.原 if 頭 == '道具' else B.換算
    try: return W.一生(s, 世界, '道具型' if 頭 == '道具' else '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; W.赤ちゃん = B.原; B.v時定数 = 1000.0
def one(job):
    s, 頭, 世界 = job; o = 一生(s, 頭, 世界)
    return (s, 頭, 世界, B.区(o, 0, 500)[2], float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]])))
腕 = [(h, w) for h in ['換算', '道具'] for w in ['依存', '無関係']]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(11699, h, w, 600)['sha256'] for h, w in 腕]; print('4腕が互いに違う:', len(set(x)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(11600, 11630) if 段 == '本' else range(11700, 11730)
    with Pool(8) as p: r = p.map(one, [(s, h, w) for h, w in 腕 for s in S])
    d = {(s, h, w): (f, g) for s, h, w, f, g in r}
    上 = lambda s, w, k: d[(s, '換算', w)][k] - d[(s, '道具', w)][k]
    res = dict(H1_無関係では小さい=int(sum(上(s, '無関係', 1) < 上(s, '依存', 1) for s in S)), H2_依存で育つ=int(sum(上(s, '依存', 1) > 上(s, '依存', 0) for s in S)), 参考_無関係で育つ=int(sum(上(s, '無関係', 1) > 上(s, '無関係', 0) for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_無関係では小さい', 'H2_依存で育つ']}
    res['上乗せ_中央値_初め育'] = {w: [round(float(np.median([上(s, w, k) for s in S])), 3) for k in range(2)] for w in ['依存', '無関係']}
    res['見られ分け_中央値'] = {f'{h}_{w}': [round(float(np.median([d[(s, h, w)][k] for s in S])), 3) for k in range(2)] for h, w in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
