import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S68R', '../S68_欠乏の後に下げる力_20261119/走らせる.py')
B, W, N, M = R.B, R.W, R.N, R.M
def 一生(s, 欠乏, 代価=0.0, 記録する=True, 寿命=8000):
    N.我慢の代価 = 代価; W.我慢の代価 = 代価   # 世界側（N）の一生が代価を渡す
    try: return R.一生(s, 欠乏, 記録する, 寿命)
    finally: N.我慢の代価 = 0.01; W.我慢の代価 = 0.01
def one(job):
    s, 欠 = job; o = 一生(s, 欠); assert o['一番'] == R.一番[0]
    Rm = np.array([R.記録[i] for i in range(8)]).transpose(1, 0, 2); 相 = o['相手列']; m = 相[7500:7700] == 0
    return (s, 欠, [float(Rm[7500:7700][m][:, k].mean()) for k in range(5)], M.P養(o, 7500, 7700))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(17299, True); b = 一生(17299, False); c = 一生(17299, True, 0.01)
        print('代価0≠代価0.01:', a['sha256'] != c['sha256'], ' 7000まで同じ:', bool((a['行動列'][:7000] == b['行動列'][:7000]).all()), ' 代価0.01＝S64 の欠乏:', c['sha256'] == M.一生(17299, '欠乏')['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(17200, 17230) if 段 == '本' else range(17300, 17330)
    with Pool(8) as p: r = p.map(one, [(s, e) for e in [False, True] for s in S])
    d = {(s, e): (v, p) for s, e, v, p in r}
    res = dict(H1_戻って喜ばせが増える=int(sum(d[(s, True)][1] > d[(s, False)][1] for s in S)), H2_癖が下げない=int(sum(d[(s, True)][0][0] >= d[(s, False)][0][0] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {('欠乏' if e else 'なし'): dict({R.名[k]: round(float(np.median([d[(s, e)][0][k] for s in S])), 4) for k in range(5)}, P養=round(float(np.median([d[(s, e)][1] for s in S])), 3)) for e in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
