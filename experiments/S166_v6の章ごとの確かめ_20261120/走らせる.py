import sys, json, os, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S166一覧', '../S166_v6の章ごとの確かめ_20261120/一覧.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def one(job): return list(job) + [float(G.one(job))]
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(35200, 35230) if 段 == '本' else range(35300, 35330)); 腕 = ['元', 'v4', 'v6']; 書 = f'結果_{段}.jsonl'
    済 = {}
    if os.path.exists(書):
        for l in open(書): x = json.loads(l); 済[(x[0], x[1], x[2])] = x[3]
    jobs = [(s, 名, w) for 名 in 腕 for w in G.世界一覧 for s in S if (s, 名, w) not in 済]
    print('残り', len(jobs), '本', file=sys.stderr, flush=True)
    with Pool(8, maxtasksperchild=1) as p, open(書, 'a') as f:
        for x in p.imap_unordered(one, jobs, chunksize=1): f.write(json.dumps(x, ensure_ascii=False) + '\n'); f.flush(); 済[(x[0], x[1], x[2])] = x[3]
    assert len(済) == len(腕) * len(G.世界一覧) * len(S), len(済)
    v = np.array([[[済[(s, 名, w)] for s in S] for w in G.世界一覧] for 名 in 腕]); 元, v4, v6 = v
    res = {'H1_S48 見られ分けを保つ': int((v6[0] >= 元[0] - 0.03).sum()), 'H2_S64 戻って甘える': int((v6[1] > 0).sum()), 'H3_S116 真ん中の視線 v6>元': int((v6[2] > 元[2]).sum()),
           'H4_S123 当たりを指す v6>元': int((v6[3] > 元[3]).sum()), 'H5_叙述的指さしが育つ': int((v6[4] > 0).sum()), 'H6_分からない時に顔を見に行く': int((v6[5] > 0).sum()), 'H7_人見知り': int((v6[6] < 0).sum())}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    章 = ['S48', 'S64増え', 'S116', 'S123', '叙述育ち', '情報探し', '人見知り取る差']
    res['参考_v6がv4以上(人見知りは未満)'] = dict(zip(章, [int((v6[j] >= v4[j]).sum()) for j in range(6)] + [int((v6[6] < v4[6]).sum())]))
    res['中央値'] = {名: dict(zip(章, [round(float(np.median(x)), 3) for x in v[k]])) for k, 名 in enumerate(腕)}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 値=v.tolist()), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
