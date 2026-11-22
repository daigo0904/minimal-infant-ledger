import sys, json, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
keep = []
class K(W.赤ちゃん):
    def __init__(s, *a): super().__init__(*a); keep.append(s)
W.赤ちゃん = K
段 = sys.argv[1]; 種 = range(4800, 4810) if 段 == '本' else range(4900, 4910)
rows = []
for s in 種:
    keep.clear(); o = W.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000); b = o['一番']
    世 = np.random.default_rng([s, 0]); 世.permutation(4); face = 世.normal(0, 1, (9, 8)); rng = np.random.default_rng(7)
    v = {k: [] for k in ['D定', 'D見養', 'D見他', 'D養', 'D他', '食養b', '食他b', '食養x', '食他x']}
    A, 相, 食 = o['行動列'], o['相手列'], o['食列']
    後 = np.array([[食[t + 1:t + 6, i].any() for i in range(8)] for t in range(4000, 7990)])
    for i, c in enumerate(keep):
        dq = c.Q[b] - np.delete(c.Q, b, axis=0).mean(axis=0); v['D定'].append(float(dq[-1]))
        for tag, ws in [('養', [0]), ('他', [j for j in range(1, 9) if j != i + 1])]:
            fs = [float(dq[:-1] @ c.感覚(face[ws[k % len(ws)]] + rng.normal(0, .3, 8))[:-1]) for k in range(200)]
            v['D見' + tag].append(float(np.mean(fs))); v['D' + tag].append(float(np.mean(fs)) + float(dq[-1]))
        a = A[4000:7990, i]; w = 相[4000:7990, i]; f = 後[:, i]
        v['食養b'].append(f[(a == b) & (w == 0)].mean()); v['食他b'].append(f[(a == b) & (w > 0)].mean())
        v['食養x'].append(f[(a != b) & (w == 0)].mean()); v['食他x'].append(f[(a != b) & (w > 0)].mean())
    r = {k: float(np.mean(x)) for k, x in v.items()}; r['種'] = s; rows.append(r); print(s, {k: round(x, 3) for k, x in r.items()}, flush=True)
med = lambda f: round(float(np.median([f(r) for r in rows])), 4)
res = dict(定数の大きさ=med(lambda r: abs(r['D定'])), 見た目の相手差=med(lambda r: abs(r['D見養'] - r['D見他'])), D養=med(lambda r: r['D養']), D他=med(lambda r: r['D他']),
           食_b_養=med(lambda r: r['食養b']), 食_b_他=med(lambda r: r['食他b']), 食_ほか_養=med(lambda r: r['食養x']), 食_ほか_他=med(lambda r: r['食他x']),
           食の差_b=med(lambda r: r['食養b'] - r['食他b']))
res['判定'] = dict(H_定数が勝つ=res['定数の大きさ'] > res['見た目の相手差'], H_目標が違う=res['食の差_b'] >= .02)
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
