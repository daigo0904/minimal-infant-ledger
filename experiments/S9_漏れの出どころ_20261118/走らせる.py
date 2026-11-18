import sys, json, numpy as np
sys.path.insert(0, '../S8_見分けが育つ_20261118'); sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W, 世界S8 as X
keep = []
段 = sys.argv[1]; 種 = range(4400, 4410) if 段 == '本' else range(4500, 4510)
def 診(s, 感覚):
    keep.clear()
    if 感覚 == '固定':
        W.感覚数 = 256; W.見た目雑音 = 0.3
        class K(W.赤ちゃん):
            def __init__(self, *a): super().__init__(*a); keep.append(self)
        orig = W.赤ちゃん; W.赤ちゃん = K
        try: o = W.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000)
        finally: W.赤ちゃん = orig
    else:
        class K(X.赤ちゃん):
            def __init__(self, *a): super().__init__(*a); keep.append(self)
        orig = X.赤ちゃん; X.赤ちゃん = K
        try: o = X.一生(s, '獲得型', '育つ', 寿命=8000, 離乳=8000)
        finally: X.赤ちゃん = orig
    世 = np.random.default_rng([s, 0]); 世.permutation(4); face = 世.normal(0, 1, (9, 8)); rng = np.random.default_rng(7); b = o['一番']
    out = {k: [] for k in ['養_Q', '養_つ', '養_両', '他_Q', '他_つ', '他_両', 'つ養', 'つ他', 'ê差他']}
    for i, c in enumerate(keep):
        c.感覚.育つ = False if hasattr(c.感覚, '育つ') else None   # 見せる間は型を動かさない
        for who, tag in [(0, '養'), (None, '他')]:
            n = {'Q': 0, 'つ': 0, '両': 0}; us = []; ed = []
            for k in range(200):
                w = who if who is not None else [j for j in range(1, 9) if j != i + 1][k % 7]
                φ = c.感覚(face[w] + rng.normal(0, 0.3, 8)); q = c.Q @ φ; ê = np.array([m.予測(φ) for m in c.評価]); u = c.つながり.予測(φ)
                n['Q'] += int(np.argmax(q)) == b; n['つ'] += int(np.argmax(2 * u * ê)) == b; n['両'] += int(np.argmax(q + 2 * u * ê)) == b
                us.append(u); ed.append(ê[b] - np.mean(np.delete(ê, b)))
            for k2 in n: out[f'{tag}_{k2}'].append(n[k2] / 200)
            out['つ' + tag].append(float(np.mean(us)))
            if tag == '他': out['ê差他'].append(float(np.mean(ed)))
    return {k: float(np.mean(v)) for k, v in out.items()}
rows = [dict(種=s, 感覚=k, **診(s, k)) for s in 種 for k in ['固定', '育つ']]
med = lambda k, f: round(float(np.median([r[f] for r in rows if r['感覚'] == k])), 3)
res = {k: {f: med(k, f) for f in ['養_Q', '養_つ', '養_両', '他_Q', '他_つ', '他_両', 'つ養', 'つ他', 'ê差他']} for k in ['固定', '育つ']}
res['判定'] = {k: dict(H_Qが漏らす=res[k]['他_Q'] >= .4, H_つながりが漏らす=res[k]['他_つ'] >= .4) for k in ['固定', '育つ']}
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
