import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S144一覧', '../S144_v3で残りの章_20261120/一覧.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def one(job): return G.one(job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(31800, 31830) if 段 == '本' else range(31900, 31930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名, w) for 名 in G.構成 for w in G.世界一覧 for s in S], chunksize=1)
    r = np.array(r).reshape(2, 2, len(S), 2); 元, v3 = r[0], r[1]
    res = {'H1_S135 v3 で交代が番と無関係の世界より大きい': int((v3[0, :, 0] > v3[0, :, 1]).sum()), 'H2_S135 v3 の交代は元から大きく崩れない（元−0.05 以上）': int((v3[0, :, 0] >= 元[0, :, 0] - 0.05).sum()),
           'H3_S90 v3 で入れ替わった後に新しいお手本を多く写す': int((v3[1, :, 0] > 0).sum())}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(S135交代の差=round(float(np.median(r[k, 0, :, 0])), 3), S135でたらめの差=round(float(np.median(r[k, 0, :, 1])), 3), S90新−古=round(float(np.median(r[k, 1, :, 0])), 3)) for k, 名 in enumerate(G.構成)}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 値=r.tolist()), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
