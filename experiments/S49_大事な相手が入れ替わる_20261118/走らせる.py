import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）。赤ちゃんの中身は B.W の定数を使う
sp = importlib.util.spec_from_file_location('S49世界', '../S49_大事な相手が入れ替わる_20261118/世界.py'); N = importlib.util.module_from_spec(sp); sp.loader.exec_module(N)
N.感覚数 = 256; N.見た目雑音 = 0.3
W = B.W
寿命 = 16000
def 一生(s, 腕, 寿命=寿命):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = B.換算
    try:
        if 腕 == '替える': return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='仲間へ', 切替=8000)
        return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def 数字(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    P養 = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)])
    合わせ = []
    for i in range(8):
        t = np.arange(max(lo, 1), hi); k = 相[t, i]; m = k > 0
        合わせ.append(float((A[t[m], i] == A[t[m] - 1, k[m] - 1]).mean()))
    return float(P養), float(np.mean(合わせ)), B.区(o, lo, hi)[2]
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, 数字(o, 7000, 8000), 数字(o, 15000, 16000), float(o['食列'][15000:16000].mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(13299, '替える', 8600); b = 一生(13299, '替えない', 8600)
        print('8000手まで同じ:', bool((a['行動列'][:8000] == b['行動列'][:8000]).all()), ' 8000〜で違う:', bool((a['行動列'][8000:] != b['行動列'][8000:]).any()))
        print('8000〜8600 の食べた割合 替える/替えない:', round(float(a['食列'][8000:].mean()), 4), round(float(b['食列'][8000:].mean()), 4), ' 合わせ 替える(8000〜):', round(数字(a, 8000, 8600)[1], 3)); sys.exit()
    段 = sys.argv[1]; S = range(13200, 13230) if 段 == '本' else range(13300, 13330)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['替えない', '替える'] for s in S])
    d = {(s, a): (x, y, f) for s, a, x, y, f in r}
    res = dict(H1_養育者の前の喜ばせが減る=int(sum(d[(s, '替える')][1][0] < d[(s, '替えない')][1][0] for s in S)), H2_仲間に合わせるが増える=int(sum(d[(s, '替える')][1][1] > d[(s, '替えない')][1][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: {w: [round(float(np.median([d[(s, a)][j][k] for s in S])), 3) for k in range(3)] for j, w in enumerate(['7000〜8000(P養,合わせ,見られ分け)', '15000〜16000'])} for a in ['替えない', '替える']}
    res['食べた割合_15000〜'] = {a: round(float(np.median([d[(s, a)][2] for s in S])), 4) for a in ['替えない', '替える']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
