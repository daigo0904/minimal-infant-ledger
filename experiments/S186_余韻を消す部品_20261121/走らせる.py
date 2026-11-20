import sys, json, numpy as np
sys.path.insert(0, '../S185_見られ分けの余韻_20261121')
from multiprocessing import Pool
import 共
v4 = dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)
腕 = {'v4': v4, 'kf0': dict(v4, kf=0.0), 'λ1': dict(v4, λ=1.0), 'kf0λ1': dict(v4, kf=0.0, λ=1.0)}
共.構成.update(腕)
def one(job): s, 名 = job; o = 共.一生(s, 名, 記憶=0.5); return (s, 名) + 共.余韻(o, 7000, 8000) + (o['sha256'],)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(38800, 38830) if 段 == '本' else range(38900, 38930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 120
    res = {'H1_食べ予測を切ると余韻': sum(d[(s, 'kf0')][0] > 0 for s in S), 'H2_癖を戻すと余韻': sum(d[(s, 'λ1')][0] > 0 for s in S),
           'H3_食べ予測のせい': sum(d[(s, 'kf0')][0] > d[(s, 'v4')][0] for s in S), 'H4_癖の重みのせい': sum(d[(s, 'λ1')][0] > d[(s, 'v4')][0] for s in S), '参考_両方を戻すと余韻': sum(d[(s, 'kf0λ1')][0] > 0 for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_食べ予測を切ると余韻', 'H2_癖を戻すと余韻', 'H3_食べ予測のせい', 'H4_癖の重みのせい']}
    res['中央値'] = {名: dict(zip(['余韻', '直後', '続き', '見られ分け'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(4)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
