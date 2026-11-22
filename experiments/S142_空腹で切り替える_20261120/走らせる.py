import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S142選び', '../S142_空腹で切り替える_20261120/選び.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
全 = dict(kf=3.0, kD=30.0, λ=0.2)
腕 = {'いつでも kJ3': dict(全, kJ=3.0), '満ちた時だけ kJ5': dict(全, kJ=5.0, 切替='J満'), '喜びなし': dict(全)}
def one(job): s, 名 = job; return (s, 名) + tuple(G.one((s, 腕[名])))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        S141 = L = None
        _s = importlib.util.spec_from_file_location('S141選び', '../S141_共同注意の喜び_20261120/選び.py'); X = importlib.util.module_from_spec(_s); _s.loader.exec_module(X)
        G.V.設定.update(kf=3.0, kD=30.0, λ=0.2, kJ=3.0, 切替=None); X.V.設定.update(kf=3.0, kD=30.0, λ=0.2, kJ=3.0)
        print('切替なしは S141 と同じ sha:', G.H.一生(31499, '褒める', 寿命=1500)['sha256'] == X.H.一生(31499, '褒める', 寿命=1500)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(31400, 31430) if 段 == '本' else range(31500, 31530)
    with Pool(8) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S])
    d = {(s, 名): v for s, 名, *v in r}
    res = {'H1_満ちた時だけでも叙述的指さしが育つ': int(sum(d[(s, '満ちた時だけ kJ5')][0] > 0 for s in S)),
           'H2_いつでもより食べ物を保つ': int(sum(d[(s, '満ちた時だけ kJ5')][2] > d[(s, 'いつでも kJ3')][2] for s in S)),
           'H3_指してばかりにならない（いつでもより指す割合が低い）': int(sum(d[(s, '満ちた時だけ kJ5')][1] < d[(s, 'いつでも kJ3')][1] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(育ち=round(float(np.median([d[(s, 名)][0] for s in S])), 3), 終わりの指す=round(float(np.median([d[(s, 名)][1] for s in S])), 3), 食べ=round(float(np.median([d[(s, 名)][2] for s in S])), 4)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
