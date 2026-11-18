import json, sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
keep = []
class K(W.赤ちゃん):
    def __init__(s, *a): super().__init__(*a); keep.append(s)
W.赤ちゃん = K
段 = sys.argv[1]; 種 = range(3300, 3310) if 段 == '本' else range(3400, 3410)
def link(s):
    世 = np.random.default_rng([s, 0]); 世.permutation(4); face = 世.normal(0, 1, (9, 8)); rng = np.random.default_rng(5)
    return float(np.mean([np.mean([c.つながり.予測(c.感覚(face[0] + rng.normal(0, W.見た目雑音, 8))) for _ in range(30)]) for c in keep]))
rows = []
for 腕, h, f in [('遅', '獲得型', 0.9999), ('速', '獲得型', 0.999), ('道具', '道具型', 0.9999)]:
    W.つながり忘却 = f
    for s in 種:
        keep.clear(); o8 = W.一生(s, '依存', h, 寿命=8000); l8 = link(s)
        keep.clear(); o = W.一生(s, '依存', h); l12 = link(s)
        assert (o['行動列'][:8000] == o8['行動列']).all()
        A, 相, b = o['行動列'], o['相手列'], o['一番']
        P = lambda lo, hi: float(np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]))
        hl = o['h列'].mean(axis=1)
        rows.append(dict(腕=腕, 種=s, P養_育=P(7000, 8000), P養_後=P(10000, 12000), 空腹_後=float(hl[100:120].mean()), つながり8000=l8, つながり12000=l12))
d = {(r['腕'], r['種']): r for r in rows}
res = dict(H_速くても残る=sum(d[('速', s)]['P養_後'] > d[('道具', s)]['P養_後'] for s in 種),
           H_遅いほど残る=sum(d[('遅', s)]['P養_後'] > d[('速', s)]['P養_後'] for s in 種))
res['判定'] = {k: res[k] >= 8 for k in ['H_速くても残る', 'H_遅いほど残る']}
res['中央値'] = {a: {k: round(float(np.median([r[k] for r in rows if r['腕'] == a])), 3) for k in ['P養_育', 'P養_後', '空腹_後', 'つながり8000', 'つながり12000']} for a in ['遅', '速', '道具']}
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
