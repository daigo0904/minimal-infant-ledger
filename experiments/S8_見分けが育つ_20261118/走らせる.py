import sys, json, numpy as np, 世界S8 as X
段 = sys.argv[1]; 種 = range(4200, 4210) if 段 == '本' else range(4300, 4310)
def 区(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return float(pa), float(po), float(pa - po)
rows = []
for s in 種:
    r = dict(種=s)
    for 種類 in ['育つ', '固定']:
        o = X.一生(s, '獲得型', 種類, 寿命=8000, 離乳=8000); r[種類 + '_sha'] = o['sha256']
        r[種類] = [区(o, k, k + 500) for k in range(0, 8000, 500)]
    assert r['育つ_sha'] != r['固定_sha']; rows.append(r); print(s, flush=True)
初 = lambda r, k: r[k][0][2]; 育 = lambda r, k: (r[k][14][2] + r[k][15][2]) / 2
res = dict(H_育つと出る=sum(初(r, '育つ') <= 育(r, '育つ') / 2 for r in rows), H_育つ大=sum(育(r, '育つ') > 育(r, '固定') for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値'] = {k: [[round(float(np.median([r[k][b][j] for r in rows])), 3) for j in range(3)] for b in range(0, 16, 2)] for k in ['育つ', '固定']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
