import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S54R', '../S54_戻ってきた養育者_20261118/走らせる.py')
R, B, W, N = M.R, M.B, M.W, M.N
def 一生(s, 腕, 寿命=24000):
    if 腕 == '戻る': return M.一生(s, 寿命)
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, R.数字(o, 7000, 8000), R.数字(o, 23000, 24000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(14499, '戻る', 9000); b = 一生(14499, 'ずっと', 9000)
        print('8000まで同じ:', bool((a['行動列'][:8000] == b['行動列'][:8000]).all()), ' 8000〜で違う:', bool((a['行動列'][8000:] != b['行動列'][8000:]).any())); sys.exit()
    段 = sys.argv[1]; S = range(14400, 14430) if 段 == '本' else range(14500, 14530)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['ずっと', '戻る'] for s in S])
    d = {(s, a): (x, y) for s, a, x, y in r}
    res = dict(H1_仲間の時期が尾を引く=int(sum(d[(s, '戻る')][1][2] < d[(s, 'ずっと')][1][2] for s in S)), H2_長生きだけでは落ちない=int(sum(d[(s, 'ずっと')][1][2] >= 0.9 * d[(s, 'ずっと')][0][2] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値_P養合わせ差'] = {a: dict(育7000=[round(float(np.median([d[(s, a)][0][k] for s in S])), 3) for k in range(3)], 終23000=[round(float(np.median([d[(s, a)][1][k] for s in S])), 3) for k in range(3)]) for a in ['ずっと', '戻る']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
