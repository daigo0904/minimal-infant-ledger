import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
def 一生(s, lr, 寿命=8000):
    W.学び率 = lr
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.学び率 = 0.05
def 区(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po)]
def one(job):
    s, lr = job; o = 一生(s, lr); _, _, 差 = W.区間の数字(o)
    return (s, lr, 差[0], [float(np.mean([区(o, 7000, 7500)[j], 区(o, 7500, 8000)[j]])) for j in range(3)], float(o['h列'][70:80].mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        print('0.01≠0.05:', 一生(10699, 0.01, 600)['sha256'] != 一生(10699, 0.05, 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(10600, 10610) if 段 == '本' else range(10700, 10710)
    with Pool(8) as p: r = p.map(one, [(s, lr) for lr in [0.05, 0.01] for s in S])
    d = {(s, lr): (f, g, h) for s, lr, f, g, h in r}
    res = dict(H1_漏れが減る=int(sum(d[(s, 0.01)][1][1] < d[(s, 0.05)][1][1] for s in S)), H2_育ちで出る=int(sum(d[(s, 0.01)][0] <= d[(s, 0.01)][1][2] / 2 for s in S)),
               H3_見られ分けが大きい=int(sum(d[(s, 0.01)][1][2] > d[(s, 0.05)][1][2] for s in S)), 参考_空腹が上がらない=int(sum(d[(s, 0.01)][2] <= d[(s, 0.05)][2] for s in S)))
    res['判定'] = {k: res[k] >= 8 for k in ['H1_漏れが減る', 'H2_育ちで出る', 'H3_見られ分けが大きい']}
    res['中央値'] = {str(lr): dict(初め差=round(float(np.median([d[(s, lr)][0] for s in S])), 3), 育_P養P他差=[round(float(np.median([d[(s, lr)][1][j] for s in S])), 3) for j in range(3)], 空腹=round(float(np.median([d[(s, lr)][2] for s in S])), 3)) for lr in [0.05, 0.01]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
