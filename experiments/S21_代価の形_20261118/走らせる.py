import sys, json, numpy as np
sys.path.insert(0, '../S17_右脳左脳_20261118')
import 脳 as B, 世界 as W
元 = B.赤ちゃん; keep = []; 報酬 = {'形': '二乗'}
class K(元):
    def __init__(self, *a): super().__init__(*a); keep.append(self)
    def 受ける(self, φ, a, q, e, 食べた, 我慢=0.0):
        super().受ける(φ, a, q, e, 食べた, 我慢)
        if 報酬['形'] == '線形':
            φ2, a2, R = self.前; self.前 = (φ2, a2, -self.h)   # 報酬を −空腹 に（代価がいつも同じ）
B.赤ちゃん = K
def 一生(s, 形, 寿命=8000):
    報酬['形'] = 形; keep.clear(); return B.一生(s, '一つ128体', 寿命)
if sys.argv[1] == '確かめ':
    B.赤ちゃん = 元; a0 = B.一生(6799, '一つ128体', 600)['sha256']; B.赤ちゃん = K
    a = 一生(6799, '二乗', 600)['sha256']; b = 一生(6799, '線形', 600)['sha256']
    print('二乗＝S19の形:', a == a0, ' 二乗≠線形:', a != b); sys.exit()
段 = sys.argv[1]; 種 = range(6800, 6810) if 段 == '本' else range(6900, 6910)
def 区(o, lo=7000, hi=8000):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po)]
def 診(s, o):
    b = o['一番']; 世 = np.random.default_rng([s, 0]); 世.permutation(4); face = 世.normal(0, 1, (9, 8)); rng = np.random.default_rng(7); out = {}
    for h in [0.3, 1.0]:
        n = tot = 0
        for i, c in enumerate(keep):
            ws = [j for j in range(1, 9) if j != i + 1]
            for k in range(35):
                for la in range(4):
                    c.直前 = np.r_[h, 0.0, 0.0, np.eye(4)[la]]; φ = c.感覚(face[ws[k % 7]] + rng.normal(0, .3, 8)); n += int(np.argmax(c.Q @ φ)) == b; tot += 1
        out[h] = n / tot
    return out
rows = []
for s in 種:
    r = dict(種=s)
    for 形 in ['二乗', '線形']:
        o = 一生(s, 形); r[形] = 区(o); d = 診(s, o); r[形 + '_Q差'] = d[0.3] - d[1.0]; r[形 + '_Q0.3'] = d[0.3]; r[形 + '_Q1.0'] = d[1.0]
    rows.append(r); print(s, {k: (round(v, 3) if isinstance(v, float) else [round(x, 3) for x in v]) for k, v in r.items() if k != '種'}, flush=True)
med = lambda k: round(float(np.median([r[k] for r in rows])), 3)
res = dict(H_漏れが下がる=sum(r['線形'][1] < r['二乗'][1] for r in rows), Q差の中央値=dict(二乗=med('二乗_Q差'), 線形=med('線形_Q差')))
res['判定'] = dict(H_漏れが下がる=res['H_漏れが下がる'] >= 8, H_空腹の差が縮む=res['Q差の中央値']['線形'] < .1)
res['中央値'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(3)] for k in ['二乗', '線形']}
res['Q中央値'] = {k: med(k) for k in ['二乗_Q0.3', '二乗_Q1.0', '線形_Q0.3', '線形_Q1.0']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
