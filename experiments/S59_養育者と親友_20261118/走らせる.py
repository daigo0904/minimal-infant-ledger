import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S50R', '../S50_相手の直前の手が見える_20261118/走らせる.py')
B, W = R.B, R.W
N = L('S59世界', '../S59_養育者と親友_20261118/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 腕, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = B.換算 if 腕 == '本物' else B.原
    try: return N.一生(s, '依存', '獲得型' if 腕 == '本物' else '道具型', 寿命=寿命, 離乳=寿命, 給餌の形='親友')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 割(o, a, b):
    A, 相, 一, 友 = o['行動列'][a:b], o['相手列'][a:b], o['一番'], o['親友の手']
    友見 = lambda i: 相[:, i] == (i + 1) % 8 + 1; 他見 = lambda i: (相[:, i] > 0) & ~友見(i)
    m = lambda f: float(np.mean(f))
    return dict(友手_友=m([(A[友見(i), i] == 友).mean() for i in range(8)]), 友手_他=m([(A[他見(i), i] == 友).mean() for i in range(8)]),
                一番_養=m([(A[相[:, i] == 0, i] == 一).mean() for i in range(8)]), 一番_友=m([(A[友見(i), i] == 一).mean() for i in range(8)]))
def one(job):
    s, 腕 = job; o = 一生(s, 腕); return (s, 腕, 割(o, 7000, 8000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(15399, '本物', 2000); A, 相, 食, 友 = o['行動列'], o['相手列'], o['食列'], o['親友の手']
        見 = np.array([[相[t, i] == (i + 1) % 8 + 1 for i in range(8)] for t in range(2000)]); 当 = 見 & (A == 友)
        print('親友の手:', 友, ' 一番:', o['一番'], ' 親友が見た手の割合:', round(float(見.mean()), 3), ' 親友の前で親友の手の時の食べた割合:', round(float(食[当].mean()), 3), ' 親友の前で他の手:', round(float(食[見 & (A != 友)].mean()), 3))
        print('本物≠道具:', o['sha256'] != 一生(15399, '道具', 2000)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(15200, 15230) if 段 == '本' else range(15300, 15330)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['本物', '道具'] for s in S])
    d = {(s, a): x for s, a, x in r}
    差 = lambda s, a: d[(s, a)]['友手_友'] - d[(s, a)]['友手_他']
    res = dict(H1_親友の前で親友の手=int(sum(差(s, '本物') > 0 for s in S)), H2_養育者の前で一番の手=int(sum(d[(s, '本物')]['一番_養'] > d[(s, '本物')]['一番_友'] for s in S)), H3_親友の分け_本物が道具より=int(sum(差(s, '本物') > 差(s, '道具') for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: {k: round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in ['友手_友', '友手_他', '一番_養', '一番_友']} for a in ['本物', '道具']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
