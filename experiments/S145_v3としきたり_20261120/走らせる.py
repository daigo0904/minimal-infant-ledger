import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
sys.path.insert(0, '../S100_多数に合わせる_20261119')
_sp = importlib.util.spec_from_file_location('S145選び', '../S145_v3としきたり_20261120/選び.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def one(job): s, 名, 型 = job; return (s, 名, 型) + G.one(job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(32000, 32030) if 段 == '本' else range(32100, 32130)
    with Pool(8) as p: r = p.map(one, [(s, 名, 型) for 名 in G.構成 for 型 in ['決まった手', 'でたらめ'] for s in S])
    d = {(s, 名, 型): v for s, 名, 型, *v in r}
    効 = lambda s, 名: d[(s, 名, '決まった手')][0] - d[(s, 名, 'でたらめ')][0]
    res = {'H1_v3 でもしきたりが代替わり後に残る': int(sum(効(s, 'v3') > 0 for s in S)), 'H2_v3 のしきたりは元から大きく崩れない（元−0.05 以上）': int(sum(d[(s, 'v3', '決まった手')][0] >= d[(s, '元', '決まった手')][0] - 0.05 for s in S)),
           'H3_v3 のほうが食べ物を保つ': int(sum(d[(s, 'v3', '決まった手')][1] > d[(s, '元', '決まった手')][1] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{名}_{型}': dict(しきたり=round(float(np.median([d[(s, 名, 型)][0] for s in S])), 3), 食べ=round(float(np.median([d[(s, 名, 型)][1] for s in S])), 4)) for 名 in G.構成 for 型 in ['決まった手', 'でたらめ']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
