import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S117頭直', '../S117_食べ予測で転移_20261119/頭直.py'); 持 = L('S117頭', '../S117_食べ予測で転移_20261119/頭.py').持ち上がり
腕 = [(直, a) for 直 in [False, True] for a in ['本物', 'ずらし']]
def one(job):
    s, 直, a = job; o = H.一生(s, 3.0, a, 直=直, 視線切替=4000)
    return (s, 直, a, float(np.mean(持(o, 3000, 4000))), float(np.mean(持(o, 3000, 4000, 相手=1))), float(np.mean(持(o, 4000, 5000, 相手=1))), float(np.mean(持(o, 7000, 8000, 相手=1))), float(np.mean(持(o, 4000, 5000))))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 27399; S111 = L('S111共2', '../S111_視線を直に_20261119/共通2.py')
        print('kf=0・直 は S111 直と同じ sha:', H.一生(s, 0.0, '本物', 直=True, 視線切替=4000, 寿命=5000)['sha256'] == S111.一生(s, 4, '本物', 寿命=5000, 学び率=0.01, 視線切替=4000, 視線直=True)['sha256'])
        y = [H.一生(s, 3.0, a, 直=直, 視線切替=4000, 寿命=3000)['sha256'] for 直, a in 腕]; print('4腕が違う:', len(set(y)) == 4)
        print({f'直{直}_{a}': [round(v, 3) for v in one((s, 直, a))[3:]] for 直, a in 腕}); sys.exit()
    段 = sys.argv[1]; S = range(27200, 27230) if 段 == '本' else range(27300, 27330)
    with Pool(8) as p: r = p.map(one, [(s, 直, a) for 直, a in 腕 for s in S])
    d = {(s, 直, a): v for s, 直, a, *v in r}
    移 = lambda s, 直: d[(s, 直, '本物')][2] - d[(s, 直, 'ずらし')][2]
    res = {'H1_直なら仲間へ移る（本物>ずらし）': int(sum(移(s, True) > 0 for s in S)), 'H2_移りは直のほうが大きい': int(sum(移(s, True) > 移(s, False) for s in S)),
           'H3_直は食べ物の出ない仲間の視線も追う（切替前>0.05）': int(sum(d[(s, True, '本物')][1] > 0.05 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['切替前_養', '切替前_仲間', '切替後1000_仲間', '終わり_仲間', '切替後1000_養']
    res['中央値'] = {f'{"直" if 直 else "混ぜる"}_{a}': {n: round(float(np.median([d[(s, 直, a)][j] for s in S])), 3) for j, n in enumerate(名)} for 直, a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
