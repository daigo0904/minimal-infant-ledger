import sys, json, numpy as np, 片側 as H
def 区(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po), float(o['h列'][lo // 100:hi // 100].mean())]
if sys.argv[1] == '確かめ':
    o = {k: H.一生(6399, k, 寿命=700, 止める時刻=500) for k in [None, '右', '左']}
    same = all((o[k]['行動列'][:500] == o[None]['行動列'][:500]).all() for k in o); diff = o['右']['sha256'] != o[None]['sha256'] != o['左']['sha256'] and o['右']['sha256'] != o['左']['sha256']
    print('止める前は同じ:', same, ' 止めた後は3つとも違う:', diff); sys.exit()
段 = sys.argv[1]; 種 = range(6400, 6410) if 段 == '本' else range(6500, 6510)
rows = []
for s in 種:
    r = dict(種=s)
    for k, name in [(None, '止めない'), ('右', '右を止める'), ('左', '左を止める')]:
        o = H.一生(s, k); r[name] = 区(o, 8000, 9000); r[name + '_前'] = 区(o, 7000, 8000)
    rows.append(r); print(s, {k: [round(x, 3) for x in v] for k, v in r.items() if k != '種'}, flush=True)
res = dict(右で見られ分けが下がる=sum(r['右を止める'][2] < r['左を止める'][2] for r in rows))
res['判定'] = dict(H=res['右で見られ分けが下がる'] >= 8)
res['中央値'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(4)] for k in ['止めない', '右を止める', '左を止める', '止めない_前']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
