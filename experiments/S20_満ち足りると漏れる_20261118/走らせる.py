import sys, json, numpy as np
sys.path.insert(0, '../S17_右脳左脳_20261118')
import 脳 as B, 世界 as W
keep = []
class K(B.赤ちゃん):
    def __init__(self, *a): super().__init__(*a); keep.append(self)
B.赤ちゃん = K
段 = sys.argv[1]; 種 = range(6600, 6610) if 段 == '本' else range(6700, 6710)
H = [0.3, 0.6, 1.0]; rows = []
for s in 種:
    keep.clear(); o = B.一生(s, '一つ128体'); b = o['一番']
    世 = np.random.default_rng([s, 0]); 世.permutation(4); face = 世.normal(0, 1, (9, 8)); rng = np.random.default_rng(7)
    r = {}
    for h in H:
        for tag in ['他', '養']:
            n = {'Q': 0, 'つ': 0, '両': 0}; tot = 0
            for i, c in enumerate(keep):
                ws = [0] if tag == '養' else [j for j in range(1, 9) if j != i + 1]
                for k in range(35):
                    for la in range(4):
                        c.直前 = np.r_[h, 0.0, 0.0, np.eye(4)[la]]
                        φ = c.感覚(face[ws[k % len(ws)]] + rng.normal(0, .3, 8)); q = c.Q @ φ; ê = np.array([m.予測(φ) for m in c.評価]); u = c.つながり.予測(φ)
                        n['Q'] += int(np.argmax(q)) == b; n['つ'] += int(np.argmax(2 * u * ê)) == b; n['両'] += int(np.argmax(q + 2 * u * ê)) == b; tot += 1
            for k2 in n: r[f'{tag}_{h}_{k2}'] = n[k2] / tot
    r['種'] = s; rows.append(r); print(s, {k: round(v, 2) for k, v in r.items() if k.startswith('他')}, flush=True)
med = lambda k: round(float(np.median([r[k] for r in rows])), 3)
res = {f'{tag}_{h}': {k2: med(f'{tag}_{h}_{k2}') for k2 in ['Q', 'つ', '両']} for tag in ['他', '養'] for h in H}
res['判定'] = dict(H_満ち足りるとQが漏らす=res['他_0.3']['Q'] >= res['他_1.0']['Q'] + .1, H_満ち足りるとつながりが漏らす=res['他_0.3']['つ'] >= res['他_1.0']['つ'] + .1)
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
