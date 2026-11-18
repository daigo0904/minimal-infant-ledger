import json
import numpy as np
import 世界 as W
本 = {(r['種'], r['条件']): r['sha256'] for r in json.load(open('結果/本.json'))['行']}
区 = 500
out = {}
for s in range(1000, 1010):
    for c in W.条件:
        r = W.一生(s, c, 記録=True)
        assert r['sha256'] == 本[(s, c)]
        A, 相 = r['行動列'], r['相手列']
        ad = []
        for b in range(0, W.寿命, 区):
            d = []
            for i in range(W.人数):
                a = A[b:b+区, i]; who = 相[b:b+区, i]
                p = np.bincount(a[who == 0], minlength=4) / max(1, (who == 0).sum())
                q = np.bincount(a[who > 0], minlength=4) / max(1, (who > 0).sum())
                d.append(0.5 * np.abs(p - q).sum())
            ad.append(float(np.mean(d)))
        out[f'{s}_{c}'] = ad
W_ = range(1000, 1010)
最後 = lambda s, c: out[f'{s}_{c}'][-1]
res = dict(
    H_見られ分け=dict(A=sum(最後(s, 'A') >= .3 for s in W_), A0=sum(最後(s, 'A0') <= .1 for s in W_)),
    H_育つと出る=sum(out[f'{s}_A'][0] < 最後(s, 'A') for s in W_),
    出てくる区間_A=[next(k for k, v in enumerate(out[f'{s}_A']) if v > 最後(s, 'A') / 2) for s in W_],
    中央値の推移={c: [round(float(np.median([out[f'{s}_{c}'][k] for s in W_])), 3) for k in range(12)] for c in W.条件})
res['H_見られ分け']['判定'] = res['H_見られ分け']['A'] >= 8 and res['H_見られ分け']['A0'] >= 8
res['H_育つと出る_判定'] = res['H_育つと出る'] >= 8
json.dump(dict(結果=res, 区間ごと=out), open('結果/誰が見ているか.json', 'x'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
