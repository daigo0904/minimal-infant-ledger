import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S59R', '../S59_養育者と親友_20261118/走らせる.py')
B, W = P.B, P.W
N = L('S61世界', '../S61_親友の好みが変わる_20261118/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 腕, 寿命=12000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='親友', 親友替え=8000 if 腕 == '替える' else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数(o, a, b):
    A, 相, 一, 旧, 新 = o['行動列'][a:b], o['相手列'][a:b], o['一番'], o['親友の手'], o['新しい親友の手']
    友 = lambda i: 相[:, i] == (i + 1) % 8 + 1; 他 = lambda i: (相[:, i] > 0) & ~友(i)
    m = lambda f: float(np.mean(f))
    return dict(新_友=m([(A[友(i), i] == 新).mean() for i in range(8)]), 旧_友=m([(A[友(i), i] == 旧).mean() for i in range(8)]), 新_他=m([(A[他(i), i] == 新).mean() for i in range(8)]),
                一番_養=m([(A[相[:, i] == 0, i] == 一).mean() for i in range(8)]), 一番_他=m([(A[他(i), i] == 一).mean() for i in range(8)]))
def one(job):
    s, 腕 = job; o = 一生(s, 腕); return (s, 腕, 数(o, 11000, 12000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(15799, '替える', 9000); b = 一生(15799, '替えない', 9000); A, 相, 食 = a['行動列'], a['相手列'], a['食列']
        見 = np.array([[相[t, i] == (i + 1) % 8 + 1 for i in range(8)] for t in range(9000)])
        print('8000まで同じ:', bool((a['行動列'][:8000] == b['行動列'][:8000]).all()), ' 8000〜で違う:', bool((a['行動列'][8000:] != b['行動列'][8000:]).any()), ' 旧/新:', a['親友の手'], a['新しい親友の手'], ' 一番:', a['一番'])
        for nm, h in [('旧', a['親友の手']), ('新', a['新しい親友の手'])]:
            print(nm, '親友の前でその手の時の食べた割合 〜8000/8000〜:', round(float(食[:8000][見[:8000] & (A[:8000] == h)].mean()), 3), round(float(食[8000:][見[8000:] & (A[8000:] == h)].mean()), 3))
        sys.exit()
    段 = sys.argv[1]; S = range(15600, 15630) if 段 == '本' else range(15700, 15730)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['替えない', '替える'] for s in S])
    d = {(s, a): x for s, a, x in r}
    養 = lambda s, a: d[(s, a)]['一番_養'] - d[(s, a)]['一番_他']
    res = dict(H1_新しい手に替える=int(sum(d[(s, '替える')]['新_友'] > d[(s, '替える')]['旧_友'] for s in S)), H2_養育者のぶんは壊れない=int(sum(養(s, '替える') >= 0.9 * 養(s, '替えない') for s in S)),
               H3_親友の前でだけ変える=int(sum(d[(s, '替える')]['新_友'] - d[(s, '替える')]['新_他'] > 0 for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: {k: round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in ['新_友', '旧_友', '新_他', '一番_養', '一番_他']} for a in ['替えない', '替える']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
