import sys, json, numpy as np
import 世界 as W
from 測る import P養
W.感覚数 = 256; W.見た目雑音 = 0.3
段 = sys.argv[1]; 種 = range(4000, 4010) if 段 == '本' else range(4100, 4110)
rows = []
for h in ['目標型', '獲得型']:
    for s in 種:
        r = dict(頭=h, 種=s); pre = None
        for 試 in ['普通', '欠乏', '飽和']:
            o = W.一生(s, '依存', h, 寿命=8700, 離乳=8000, 試し=None if 試 == '普通' else 試)
            r[試] = P養(o, 8500, 8600)
            p = o['行動列'][:8000].tobytes(); assert pre is None or p == pre; pre = p
        rows.append(r); print(s, h, r, flush=True)
med = lambda h, f: float(np.median([f(r) for r in rows if r['頭'] == h]))
欠 = lambda r: r['欠乏'] - r['普通']; 飽 = lambda r: r['普通'] - r['飽和']
res = dict(欠乏_目標型=dict(正=sum(欠(r) > 0 for r in rows if r['頭'] == '目標型'), 中央値=round(med('目標型', 欠), 3)),
           欠乏_獲得型=dict(中央値=round(med('獲得型', 欠), 3)),
           飽和_目標型=dict(正=sum(飽(r) > 0 for r in rows if r['頭'] == '目標型'), 中央値=round(med('目標型', 飽), 3)),
           飽和_獲得型=dict(中央値=round(med('獲得型', 飽), 3)))
res['判定'] = dict(H_欠乏_目標型=res['欠乏_目標型']['正'] >= 8 and res['欠乏_目標型']['中央値'] >= .05, H_欠乏_獲得型=res['欠乏_獲得型']['中央値'] < .05,
                 H_飽和_目標型=res['飽和_目標型']['正'] >= 8 and res['飽和_目標型']['中央値'] >= .05, H_飽和_獲得型=res['飽和_獲得型']['中央値'] < .05)
res['中央値P養'] = {h: {k: round(float(np.median([r[k] for r in rows if r['頭'] == h])), 3) for k in ['普通', '欠乏', '飽和']} for h in ['目標型', '獲得型']}
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
