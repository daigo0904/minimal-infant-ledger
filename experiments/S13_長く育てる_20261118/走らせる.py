import sys, json, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
段 = sys.argv[1]; 頭 = sys.argv[2]; 種 = range(5200, 5210) if 段 == '本' else range(5300, 5310)
rows = []
for s in 種:
    o = W.一生(s, '依存', 頭, 寿命=24000, 離乳=24000); A, 相, b = o['行動列'], o['相手列'], o['一番']
    區 = []
    for lo in range(0, 24000, 4000):
        pa = np.mean([(A[lo:lo + 4000, i][相[lo:lo + 4000, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:lo + 4000, i][相[lo:lo + 4000, i] > 0] == b).mean() for i in range(8)])
        區.append([float(pa), float(po), float(pa - po)])
    rows.append(dict(種=s, 区間=區)); print(s, [[round(x, 2) for x in r] for r in 區], flush=True)
res = dict(H_漏れが減る=sum(r['区間'][5][1] < r['区間'][1][1] for r in rows), H_見られ分けが育つ=sum(r['区間'][5][2] > r['区間'][1][2] for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値'] = [[round(float(np.median([r['区間'][k][j] for r in rows])), 3) for j in range(3)] for k in range(6)]
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}_{頭}.json', 'x'), ensure_ascii=False, indent=1)
