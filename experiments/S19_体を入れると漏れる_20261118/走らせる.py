import sys, json, numpy as np
sys.path.insert(0, '../S17_右脳左脳_20261118')
import 脳 as B
空腹記録 = []
class K(B.赤ちゃん):
    def 選ぶ(self, φ):
        空腹記録.append(self.h); return super().選ぶ(φ)
B.赤ちゃん = K
段 = sys.argv[1]; 種 = range(6600, 6610) if 段 == '本' else range(6700, 6710)
def 区(o, H, lo=7000, hi=8000):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    上, 下 = [], []
    for i in range(8):
        h = H[lo:hi, i]; m = np.median(h); a = A[lo:hi, i]; w = 相[lo:hi, i] > 0
        上.append((a[w & (h > m)] == b).mean()); 下.append((a[w & (h <= m)] == b).mean())
    return [float(pa), float(po), float(pa - po), float(np.mean(上)), float(np.mean(下))]
rows = []
for s in 種:
    r = dict(種=s)
    for 腕 in ['一つ128', '一つ128体']:
        空腹記録.clear(); o = B.一生(s, 腕); H = np.array(空腹記録).reshape(8000, 8); r[腕] = 区(o, H)
    rows.append(r); print(s, {k: [round(x, 3) for x in v] for k, v in r.items() if k != '種'}, flush=True)
res = dict(H_漏れが増える=sum(r['一つ128体'][1] > r['一つ128'][1] for r in rows), H_見られ分けが小さい=sum(r['一つ128体'][2] < r['一つ128'][2] for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値[P養,P他,差,P他_空腹上,P他_空腹下]'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(5)] for k in ['一つ128', '一つ128体']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
