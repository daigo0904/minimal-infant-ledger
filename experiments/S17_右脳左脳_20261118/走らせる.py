import sys, json, numpy as np, 脳 as B
if sys.argv[1] == '確かめ':
    sh = {a: B.一生(5999, a, 600)['sha256'] for a in B.腕の種類}
    print('6つの腕がすべて違う一生:', len(set(sh.values())) == 6); sys.exit()
段 = sys.argv[1]; 種 = range(6000, 6010) if 段 == '本' else range(6100, 6110)
def 区(o, lo=7000, hi=8000):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po)]
rows = []
for s in 種:
    r = dict(種=s, **{a: 区(B.一生(s, a)) for a in B.腕の種類}); rows.append(r); print(s, {a: [round(x, 3) for x in r[a]] for a in B.腕の種類}, flush=True)
比べ = [('役割', '一つ128体'), ('見方', '一つ128'), ('脳梁あり', '脳梁なし'), ('脳梁あり', '一つ128')]
res = {f'{x}対{y}': dict(見られ分けが大きい=sum(r[x][2] > r[y][2] for r in rows), 漏れが少ない=sum(r[x][1] < r[y][1] for r in rows)) for x, y in 比べ}
for k in res: res[k]['判定'] = dict(見られ分け=res[k]['見られ分けが大きい'] >= 8, 漏れ=res[k]['漏れが少ない'] >= 8)
res['中央値'] = {a: [round(float(np.median([r[a][j] for r in rows])), 3) for j in range(3)] for a in B.腕の種類}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
