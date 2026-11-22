import sys, json, numpy as np, 二つの脳 as T
sys.path.insert(0, '../S17_右脳左脳_20261118'); import 脳 as B
if sys.argv[1] == '確かめ':
    sh = {a: T.一生(6199, a, 600)['sha256'] for a in T.腕の種類}
    print('5つの腕がすべて違う:', len(set(sh.values())) == 5, ' 共有の形＝S17:', sh['共有見方'] == B.一生(6199, '見方', 600)['sha256'] and sh['共有128'] == B.一生(6199, '一つ128', 600)['sha256']); sys.exit()
段 = sys.argv[1]; 種 = range(6200, 6210) if 段 == '本' else range(6300, 6310)
def 区(o, lo=7000, hi=8000):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po)]
rows = []
for s in 種:
    r = dict(種=s, **{a: 区(T.一生(s, a)) for a in T.腕の種類}); rows.append(r); print(s, {a: [round(x, 3) for x in r[a]] for a in T.腕の種類}, flush=True)
比べ = [('別々', '共有見方'), ('別々・右が速い', '別々'), ('別々', '別々・脳梁なし'), ('別々', '共有128')]
res = {f'{x}対{y}': dict(見られ分けが大きい=sum(r[x][2] > r[y][2] for r in rows), 漏れが少ない=sum(r[x][1] < r[y][1] for r in rows)) for x, y in 比べ}
for k in list(res): res[k]['判定'] = dict(見られ分け=res[k]['見られ分けが大きい'] >= 8, 漏れ=res[k]['漏れが少ない'] >= 8)
res['中央値'] = {a: [round(float(np.median([r[a][j] for r in rows])), 3) for j in range(3)] for a in T.腕の種類}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
