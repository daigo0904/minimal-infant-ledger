import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S59R', '../S59_養育者と親友_20261118/走らせる.py')
Z = L('S47R', '../S47_本物とずらし_20261118/走らせる.py')
B, W, N = P.B, P.W, P.N
assert Z.B is B
def 一生(s, 腕, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; Z.ずらし幅[0] = 1; Z.直前の食.clear()
    N.赤ちゃん = B.換算 if 腕 == '本物' else Z.ずらし
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='親友')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def one(job):
    s, 腕 = job; o = 一生(s, 腕); return (s, 腕, P.割(o, 7000, 8000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(15599, '本物', 600); b = 一生(15599, 'ずらし', 600)
        print('本物≠ずらし:', a['sha256'] != b['sha256'], ' 本物＝S59 の本物:', a['sha256'] == P.一生(15599, '本物', 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(15400, 15430) if 段 == '本' else range(15500, 15530)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['本物', 'ずらし'] for s in S])
    d = {(s, a): x for s, a, x in r}
    友 = lambda s, a: d[(s, a)]['友手_友'] - d[(s, a)]['友手_他']; 養 = lambda s, a: d[(s, a)]['一番_養'] - d[(s, a)]['一番_友']
    res = dict(H1_親友の分け本物が大=int(sum(友(s, '本物') > 友(s, 'ずらし') for s in S)), H2_養育者と親友の分け本物が大=int(sum(養(s, '本物') > 養(s, 'ずらし') for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: {k: round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in ['友手_友', '友手_他', '一番_養', '一番_友']} for a in ['本物', 'ずらし']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
