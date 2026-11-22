import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S64R', '../S64_構われないと_20261118/走らせる.py')
B, W, N = M.B, M.W, M.N
def 一生(s, 手, 欠乏, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.行動数 = 手; W.行動数 = 手; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * (手 - 4); N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]
def one(job):
    s, 手, 欠 = job; o = 一生(s, 手, 欠); return (s, 手, 欠, M.P養(o, 7500, 7700), None if 欠 else B.区(o, 7000, 7500)[2])
腕 = [(手, 欠) for 手 in [4, 16] for 欠 in [False, True]]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(22999, 16, True, 7600); b = 一生(22999, 16, False, 7600)
        print('16手を使う:', len(set(a['行動列'].ravel().tolist())), ' 7000まで同じ:', bool((a['行動列'][:7000] == b['行動列'][:7000]).all()), ' 4手＝S64:', 一生(22999, 4, True)['sha256'] == M.一生(22999, '欠乏')['sha256'])
        print('手16 の育った後の P養（欠乏なし 7000〜7500）:', round(M.P養(b, 7000, 7500), 3)); sys.exit()
    段 = sys.argv[1]; S = range(22800, 22830) if 段 == '本' else range(22900, 22930)
    with Pool(8) as p: r = p.map(one, [(s, 手, 欠) for 手, 欠 in 腕 for s in S])
    d = {(s, 手, 欠): (p_, a) for s, 手, 欠, p_, a in r}
    増 = lambda s, 手: d[(s, 手, True)][0] - d[(s, 手, False)][0]
    res = dict(H1_手16で戻って増える=int(sum(増(s, 16) > 0 for s in S)), H2_増えが手16で大きい=int(sum(増(s, 16) > 増(s, 4) for s in S)), 参考_手4で戻って増える=int(sum(増(s, 4) > 0 for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_手16で戻って増える', 'H2_増えが手16で大きい']}
    res['中央値'] = {f'手{手}': dict(増え=round(float(np.median([増(s, 手) for s in S])), 3), P養_なし=round(float(np.median([d[(s, 手, False)][0] for s in S])), 3), 見られ分け=round(float(np.median([d[(s, 手, False)][1] for s in S])), 3)) for 手 in [4, 16]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
