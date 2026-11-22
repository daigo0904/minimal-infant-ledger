import sys, json, numpy as np
sys.path.insert(0, '../S109_共同注意_20261119')
from multiprocessing import Pool
import 共通2 as C
B, W, N = C.B, C.W, C.N
記録 = {}
class 記録つき(B.換算):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番号 = i; s.手数 = 0; 記録[i] = dict(ê=np.zeros((8000, 4)), u=np.zeros(8000), q=np.zeros((8000, 4)))
    def 選ぶ(s, φ):
        t = s.手数; s.手数 += 1; a, q, ê = super().選ぶ(φ)
        if t < 8000: 記録[s.番号]['ê'][t] = ê; 記録[s.番号]['u'][t] = s.つながり.予測(φ); 記録[s.番号]['q'][t] = q
        return a, q, ê
def 一生(s):
    記録.clear(); 原 = B.換算; B.換算 = 記録つき
    try: o = C.一生(s, 4, '本物', 学び率=0.01)
    finally: B.換算 = 原
    return o, {i: dict(v) for i, v in 記録.items()}
def one(s, lo=7000, hi=8000):
    o, R = 一生(s); 相, 視 = o['相手列'], o['視線列']; 好 = np.array(o['好み'])
    差, 他差, u養, u他, 選差 = [], [], [], [], []
    for i in range(8):
        m = np.arange(lo, hi)[相[lo:hi, i] == 0]; g = 視[m, 0]; E = R[i]['ê'][m]; U = R[i]['u'][m]
        超 = E - 好[None, :]; 差.append(float(np.mean(超[np.arange(len(m)), g])))
        mask = np.ones_like(超, dtype=bool); mask[np.arange(len(m)), g] = False; 他差.append(float(超[mask].mean()))
        u養.append(float(U.mean())); u他.append(float(R[i]['u'][np.arange(lo, hi)[相[lo:hi, i] > 0]].mean()))
        項 = U[:, None] * E; 選差.append(float(np.mean(項[np.arange(len(m)), g] - 項.mean(1))))
    return (s, float(np.mean(差)), float(np.mean(他差)), float(np.mean(u養)), float(np.mean(u他)), float(np.mean(選差)), float(o['sha256'] == o['sha256']))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 26799; o, R = 一生(s); print('記録つきは S109 と同じ sha:', o['sha256'] == C.一生(s, 4, '本物', 学び率=0.01)['sha256'])
        print('記録の大きさ:', R[0]['ê'].shape, ' 7999 手目まで埋まる:', bool(np.abs(R[0]['ê'][7999]).sum() > 0))
        print('1世界（ê−好み の 視線の手／他の手、u 養育者／仲間、u·ê の視線の手の上乗せ）:', [round(v, 3) for v in one(s)[1:6]]); sys.exit()
    段 = sys.argv[1]; S = range(26600, 26630) if 段 == '本' else range(26700, 26730)
    with Pool(8) as p: r = p.map(one, list(S))
    res = {'H1_視線の手の評価の予測が高く出る': int(sum(x[1] > x[2] for x in r)), 'H2_養育者へのつながりが正': int(sum(x[3] > 0 for x in r)), 'H3_u·ê が視線の手を推す': int(sum(x[5] > 0 for x in r))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = dict(視線の手のê超え=round(float(np.median([x[1] for x in r])), 3), 他の手のê超え=round(float(np.median([x[2] for x in r])), 3), u養育者=round(float(np.median([x[3] for x in r])), 4), u仲間=round(float(np.median([x[4] for x in r])), 4), 視線の手の項の上乗せ=round(float(np.median([x[5] for x in r])), 4))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
