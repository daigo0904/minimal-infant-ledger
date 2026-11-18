import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S34_Qを遅く_20261118')
import 頭 as H   # 換算型（c=30）×その手だけ、学び率を変える
def one(job):
    s, lr = job; o = H.一生(s, lr)
    g = [float(np.mean([H.B.区(o, 7000, 7500)[j], H.B.区(o, 7500, 8000)[j]])) for j in range(3)]
    return (s, lr, g, float(o['h列'][70:80].mean()), float(o['食列'][7000:8000].mean()))
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(11000, 11030) if 段 == '本' else range(11100, 11130)
    with Pool(8) as p: r = p.map(one, [(s, lr) for lr in [0.05, 0.01] for s in S])
    d = {(s, lr): (g, h, f) for s, lr, g, h, f in r}
    res = dict(H1_飢える=int(sum(d[(s, 0.01)][1] > d[(s, 0.05)][1] for s in S)), H2_漏れが減る=int(sum(d[(s, 0.01)][0][1] < d[(s, 0.05)][0][1] for s in S)))
    res['判定'] = dict(H1_飢える=res['H1_飢える'] >= 20, H2_漏れが減る=res['H2_漏れが減る'] >= 24)
    res['記述'] = dict(空腹の差の中央値=round(float(np.median([d[(s, 0.01)][1] - d[(s, 0.05)][1] for s in S])), 4),
                     食べた割合の差の中央値=round(float(np.median([d[(s, 0.01)][2] - d[(s, 0.05)][2] for s in S])), 4),
                     空腹=[round(float(np.median([d[(s, lr)][1] for s in S])), 3) for lr in [0.05, 0.01]], P他=[round(float(np.median([d[(s, lr)][0][1] for s in S])), 3) for lr in [0.05, 0.01]])
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
