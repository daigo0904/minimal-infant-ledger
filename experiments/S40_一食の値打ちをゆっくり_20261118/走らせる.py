import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
子 = []
class 見る(B.換算):
    def __init__(s, *a): super().__init__(*a); 子.append(s)
def 一生(s, 腕, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0 if 腕 == '5000' else 1000.0
    W.赤ちゃん = B.原 if 腕 == '道具' else 見る; 子.clear()
    try: return W.一生(s, '依存', '道具型' if 腕 == '道具' else '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; W.赤ちゃん = B.原; B.v時定数 = 1000.0
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, B.区(o, 0, 500)[2], float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]])))
腕 = ['1000', '5000', '道具']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        v = {}
        for a in ['1000', '5000']:
            v[a] = [float(np.median([c.v食 for c in (一生(s, a, 500), 子)[1]])) for s in range(900, 905)]
        print('500手時点の v食 中央値 1000:', [round(x, 3) for x in v['1000']], ' 5000:', [round(x, 3) for x in v['5000']], ' 5000 が小さい:', sum(a > b for a, b in zip(v['1000'], v['5000'])), '/5')
        x = [一生(11499, a, 600)['sha256'] for a in 腕]; print('3腕が互いに違う:', len(set(x)) == 3); sys.exit()
    段 = sys.argv[1]; S = range(11400, 11430) if 段 == '本' else range(11500, 11530)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): (f, g) for s, a, f, g in r}
    res = dict(H1_上乗せが育つ=int(sum(d[(s, '5000')][1] - d[(s, '道具')][1] > d[(s, '5000')][0] - d[(s, '道具')][0] for s in S)),
               H2_大きさを保つ=int(sum(d[(s, '5000')][1] >= 0.9 * d[(s, '1000')][1] for s in S)),
               参考_1000の上乗せが育つ=int(sum(d[(s, '1000')][1] - d[(s, '道具')][1] > d[(s, '1000')][0] - d[(s, '道具')][0] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_上乗せが育つ', 'H2_大きさを保つ']}
    res['中央値'] = {a: [round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in range(2)] for a in 腕}
    res['上乗せ_中央値'] = {a: [round(float(np.median([d[(s, a)][k] - d[(s, '道具')][k] for s in S])), 3) for k in range(2)] for a in ['1000', '5000']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
