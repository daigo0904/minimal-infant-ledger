import json, sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
keep = []
class K(W.赤ちゃん):
    def __init__(s, *a): super().__init__(*a); keep.append(s)
W.赤ちゃん = K
rows = []
for 腕, 給 in [('そのまま', 0.08), ('給餌の差2倍', 0.16)]:
    W.気に入りの給餌 = 給
    for h in ['獲得型', '道具型']:
        for s in range(2800, 2810):
            keep.clear(); o = W.一生(s, '依存', h, 寿命=8000, 離乳=8000)
            A, 相, b = o['行動列'][7000:8000], o['相手列'][7000:8000], o['一番']
            P養 = float(np.mean([(A[:, i][相[:, i] == 0] == b).mean() for i in range(8)]))
            P他 = float(np.mean([(A[:, i][相[:, i] > 0] == b).mean() for i in range(8)]))
            世 = np.random.default_rng([s, 0]); 世.permutation(4); face = 世.normal(0, 1, (9, 8)); rng = np.random.default_rng(5)
            uc = float(np.mean([np.mean([c.つながり.予測(c.感覚(face[0] + rng.normal(0, .6, 8))) for _ in range(50)]) for c in keep]))
            up = float(np.mean([np.mean([c.つながり.予測(c.感覚(face[1 + (k % 8)] + rng.normal(0, .6, 8))) for k in range(50)]) for c in keep]))
            rows.append(dict(腕=腕, 頭=h, 種=s, P養=P養, P他=P他, 差=P養 - P他, つながり養=uc, つながり他=up, 食=float(o['食列'].mean())))
med = lambda 腕, h, k: round(float(np.median([r[k] for r in rows if r['腕'] == 腕 and r['頭'] == h])), 3)
res = {f'{a}×{h}': {k: med(a, h, k) for k in ['P養', 'P他', '差', 'つながり養', 'つながり他', '食']} for a in ['そのまま', '給餌の差2倍'] for h in ['獲得型', '道具型']}
g = res['そのまま×獲得型']; t = res['そのまま×道具型']
res['判定'] = dict(漏れ=g['P他'] >= .35, 見分け=(g['つながり養'] - g['つながり他']) <= .05, 疎さ=(res['給餌の差2倍×獲得型']['差'] - g['差']) >= .05, 道具の上乗せ=t['P他'] >= .35)
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open('結果.json', 'x'), ensure_ascii=False, indent=1)
