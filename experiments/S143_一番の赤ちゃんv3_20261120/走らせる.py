import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S143一覧', '../S143_一番の赤ちゃんv3_20261120/一覧.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def one(job): return G.one(job)
def 並び(job): return G.並び(job)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        with Pool(5, maxtasksperchild=1) as p:
            a = p.map(並び, [(w, {}) for w in G.世界一覧], chunksize=1); b = p.map(並び, [(w, G.構成['v3']) for w in G.世界一覧], chunksize=1)
        print('v3 で手が変わる:', dict(zip(G.世界一覧, [x != y for x, y in zip(a, b)]))); sys.exit()
    段 = sys.argv[1]; S = list(range(31600, 31630) if 段 == '本' else range(31700, 31730))
    jobs = [(s, 名, w) for 名 in ['元', 'v3'] for w in G.世界一覧 for s in S]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, jobs, chunksize=1)
    v = np.array(r).reshape(2, len(G.世界一覧), len(S)); 元, 全 = v[0], v[1]
    res = {'H1_S48 見られ分けを保つ（元−0.03 以上）': int((全[0] >= 元[0] - 0.03).sum()), 'H2_S64 戻って甘える（増え>0）': int((全[1] > 0).sum()),
           'H3_S116 真ん中の視線追い（v3>元）': int((全[2] > 元[2]).sum()), 'H4_S123 当たりを指す（v3>元）': int((全[3] > 元[3]).sum()), 'H5_叙述的指さしが育つ（育ち>0）': int((全[4] > 0).sum())}
    res['判定'] = {k: v_ >= 20 for k, v_ in res.items()}
    res['中央値'] = {名: dict(zip(['S48', 'S64増え', 'S116', 'S123', '叙述育ち'], [round(float(np.median(x)), 3) for x in v[k]])) for k, 名 in enumerate(['元', 'v3'])}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 値=v.tolist()), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
