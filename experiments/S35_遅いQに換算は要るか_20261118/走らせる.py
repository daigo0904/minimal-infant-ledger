import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
def 一生(s, 頭, lr, 寿命=8000):
    W.学び率 = lr; W.赤ちゃん = B.換算 if 頭 == '換算' else B.原
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; W.赤ちゃん = B.原
def one(job):
    s, h, lr = job; o = 一生(s, h, lr)
    return (s, h, lr, [float(np.mean([B.区(o, 7000, 7500)[j], B.区(o, 7500, 8000)[j]])) for j in range(3)])
腕 = [(h, lr) for h in ['元', '換算'] for lr in [0.05, 0.01]]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(10499, h, lr, 600)['sha256'] for h, lr in 腕]; print('4腕が互いに違う:', len(set(x)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(10400, 10410) if 段 == '本' else range(10500, 10510)
    with Pool(8) as p: r = p.map(one, [(s, h, lr) for h, lr in 腕 for s in S])
    d = {(s, h, lr): g for s, h, lr, g in r}
    減 = lambda s, h: d[(s, h, 0.05)][1] - d[(s, h, 0.01)][1]
    res = dict(H1_元でも減る=int(sum(減(s, '元') > 0 for s in S)), H2_換算で多く減る=int(sum(減(s, '換算') > 減(s, '元') for s in S)), 参考_換算で減る=int(sum(減(s, '換算') > 0 for s in S)))
    res['判定'] = {k: res[k] >= 8 for k in ['H1_元でも減る', 'H2_換算で多く減る']}
    res['中央値_育_P養P他差'] = {f'{h}_{lr}': [round(float(np.median([d[(s, h, lr)][j] for s in S])), 3) for j in range(3)] for h, lr in 腕}
    res['漏れの減り_中央値'] = {h: round(float(np.median([減(s, h) for s in S])), 3) for h in ['元', '換算']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
