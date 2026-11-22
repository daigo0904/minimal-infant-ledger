import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S120食頭', '../S120_視線で当たりを早く_20261119/食頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
腕 = ['見える', 'ずらし', '見えない']
def one(job):
    s, a = job; o = H.一生(s, 3.0, a, 直=False)
    return (s, a, H.乗り換え(o, 相手=0), H.乗り換え(o, 相手=1), H.乗り換え(o, 窓=1000), float(o['食列'][2000:].mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 27799; o = H.一生(s, 3.0, '見える', 直=False, 寿命=3000); 当 = np.array(o['当たり'])
        print('養育者の視線＝今の当たり:', bool((o['視線列'][:, 0] == 当[np.arange(3000) // 1000]).all()), ' 仲間の視線は乱数（当たりと一致 ≈0.25）:', round(float((o['視線列'][:, 1] == 当[np.arange(3000) // 1000]).mean()), 3))
        o2 = H.一生(s, 3.0, 'ずらし', 直=False, 寿命=3000); print('ずらしの養育者の視線と当たりの一致 ≈0.25:', round(float((o2['視線列'][:, 0] == 当[np.arange(3000) // 1000]).mean()), 3))
        y = [H.一生(s, 3.0, a, 直=False, 寿命=3000)['sha256'] for a in 腕]; print('3腕が違う:', len(set(y)) == 3)
        print({a: [round(v, 3) for v in one((s, a))[2:]] for a in 腕}); sys.exit()
    段 = sys.argv[1]; S = range(27600, 27630) if 段 == '本' else range(27700, 27730)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): v for s, a, *v in r}
    res = {'H1_視線が見えると養育者の前で乗り換えが速い（見える>ずらし）': int(sum(d[(s, '見える')][0] > d[(s, 'ずらし')][0] for s in S)),
           'H2_手がかりのない仲間の前でも速い（見える>見えない）': int(sum(d[(s, '見える')][1] > d[(s, '見えない')][1] for s in S)),
           'H3_食べ物が増える（見える>見えない）': int(sum(d[(s, '見える')][3] > d[(s, '見えない')][3] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(切替後200手_養育者前=round(float(np.median([d[(s, a)][0] for s in S])), 3), 切替後200手_仲間前=round(float(np.median([d[(s, a)][1] for s in S])), 3), 切替後1000手=round(float(np.median([d[(s, a)][2] for s in S])), 3), 食べ=round(float(np.median([d[(s, a)][3] for s in S])), 4)) for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
