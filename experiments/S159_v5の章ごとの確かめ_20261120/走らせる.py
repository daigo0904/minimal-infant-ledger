import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S159一覧', '../S159_v5の章ごとの確かめ_20261120/一覧.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def one(job): return G.one(job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(34200, 34230) if 段 == '本' else range(34300, 34330)); 腕 = ['元', 'v4', 'v5']
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名, w) for 名 in 腕 for w in G.世界一覧 for s in S], chunksize=1)
    v = np.array(r, dtype=float).reshape(3, len(G.世界一覧), len(S)); 元, v4, v5 = v
    res = {'H1_S48 見られ分けを保つ': int((v5[0] >= 元[0] - 0.03).sum()), 'H2_S64 戻って甘える': int((v5[1] > 0).sum()), 'H3_S116 真ん中の視線 v5>元': int((v5[2] > 元[2]).sum()),
           'H4_S123 当たりを指す v5>元': int((v5[3] > 元[3]).sum()), 'H5_叙述的指さしが育つ': int((v5[4] > 0).sum()), 'H6_分からない時に顔を見に行く': int((v5[5] > 0).sum())}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    章 = ['S48', 'S64増え', 'S116', 'S123', '叙述育ち', '情報探し']
    res['参考_v5>=v4'] = dict(zip(章, [int((v5[j] >= v4[j]).sum()) for j in range(6)]))
    res['中央値'] = {名: dict(zip(章, [round(float(np.median(x)), 3) for x in v[k]])) for k, 名 in enumerate(腕)}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 値=v.tolist()), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
