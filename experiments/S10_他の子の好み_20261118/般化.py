import json, numpy as np
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
keep = []
class K(W.赤ちゃん):
    def __init__(s, *a): super().__init__(*a); keep.append(s)
W.赤ちゃん = K
res = {}
for 他 in ['同じ', '固定好み']:
    vals = {'他': [], '養': []}
    for s in range(4600, 4610):
        keep.clear(); o = W.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 他の子=他); b = o['一番']
        世 = np.random.default_rng([s, 0]); 世.permutation(4); face = 世.normal(0, 1, (9, 8)); rng = np.random.default_rng(7)
        for tag, ws in [('養', [0]), ('他', list(range(1, 9)))]:
            d = []
            for i, c in enumerate(keep):
                for w in ws:
                    if w == i + 1: continue
                    for _ in range(10):
                        ê = np.array([m.予測(c.感覚(face[w] + rng.normal(0, .3, 8))) for m in c.評価]); d.append(ê[b] - np.mean(np.delete(ê, b)))
            vals[tag].append(float(np.mean(d)))
    res[他] = {k: round(float(np.median(v)), 3) for k, v in vals.items()}
res['判定'] = dict(H_般化=res['固定好み']['他'] >= .2)
print(json.dumps(res, ensure_ascii=False)); json.dump(res, open('結果_般化.json', 'x'), ensure_ascii=False, indent=1)
