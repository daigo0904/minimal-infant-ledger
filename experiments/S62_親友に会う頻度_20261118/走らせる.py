import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S59R', '../S59_養育者と親友_20261118/走らせる.py')
B, W = P.B, P.W
N = L('S62世界', '../S62_親友に会う頻度_20261118/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 腕, 寿命=12000, 頻度=None):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='親友', 親友替え=8000 if 腕 == '替える' else None, 親友の頻度=頻度)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 数(o, a, b):
    A, 相, 一, 旧, 新 = o['行動列'][a:b], o['相手列'][a:b], o['一番'], o['親友の手'], o['新しい親友の手']
    友 = lambda i: 相[:, i] == (i + 1) % 8 + 1; 他 = lambda i: (相[:, i] > 0) & ~友(i)
    m = lambda f: float(np.mean(f))
    return dict(新_友=m([(A[友(i), i] == 新).mean() for i in range(8)]), 旧_友=m([(A[友(i), i] == 旧).mean() for i in range(8)]), 新_他=m([(A[他(i), i] == 新).mean() for i in range(8)]),
                一番_養=m([(A[相[:, i] == 0, i] == 一).mean() for i in range(8)]), 一番_他=m([(A[他(i), i] == 一).mean() for i in range(8)]))
def one(job):
    s, f = job; o = 一生(s, '替える', 頻度=f); return (s, f, 数(o, 11000, 12000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        for f in [1 / 7, 0.5]:
            o = 一生(15999, '替える', 300, f); 相 = o['相手列']
            print('頻度', round(f, 3), ' 親友が見る手の割合:', round(float(np.mean([[相[t, i] == (i + 1) % 8 + 1 for i in range(8)] for t in range(300)])), 3))
        a = 一生(15999, '替える', 600, 1 / 7); b = 一生(15999, '替える', 600, None)
        print('頻度1/7 の新しい作り＝元の並び:', bool((a['相手列'] == b['相手列']).all()), '（違えば両腕とも新しい作りで比べる）')
        print('1/7≠0.5:', a['sha256'] != 一生(15999, '替える', 600, 0.5)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(15800, 15830) if 段 == '本' else range(15900, 15930)
    F = [1 / 7, 0.5]
    with Pool(8) as p: r = p.map(one, [(s, f) for f in F for s in S])
    d = {(s, f): x for s, f, x in r}
    差 = lambda s, f: d[(s, f)]['新_友'] - d[(s, f)]['旧_友']
    res = dict(H1_頻度0_5で新しい手が上=int(sum(差(s, 0.5) > 0 for s in S)), H2_入れ替わりが頻度で速い=int(sum(差(s, 0.5) > 差(s, F[0]) for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {str(round(f, 3)): {k: round(float(np.median([d[(s, f)][k] for s in S])), 3) for k in ['新_友', '旧_友', '新_他', '一番_養', '一番_他']} for f in F}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
