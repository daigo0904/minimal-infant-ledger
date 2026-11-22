import json, sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
段 = sys.argv[1]; 種 = range(3100, 3110) if 段 == '本' else range(3200, 3210)
rows = []
for h in ['獲得型', '道具型']:
    for s in 種:
        o = W.一生(s, '依存', h); A, 相, b = o['行動列'], o['相手列'], o['一番']
        def P(lo, hi, who):
            return float(np.mean([(A[lo:hi, i][(相[lo:hi, i] == 0) if who == 0 else (相[lo:hi, i] > 0)] == b).mean() for i in range(8)]))
        hl = o['h列'].mean(axis=1)  # 100手ごと
        rows.append(dict(頭=h, 種=s, P養_育=P(7000, 8000, 0), P他_育=P(7000, 8000, 1), P養_後=P(10000, 12000, 0), P他_後=P(10000, 12000, 1),
                         空腹_前=float(hl[:80].mean()), 空腹_後=float(hl[100:120].mean()), sha256=o['sha256']))
d = {(r['頭'], r['種']): r for r in rows}
差 = lambda r, k: r['P養_' + k] - r['P他_' + k]
res = dict(H5a=sum(d[('獲得型', s)]['P養_後'] > d[('道具型', s)]['P養_後'] for s in 種),
           H5b=sum(d[('獲得型', s)]['空腹_後'] > d[('道具型', s)]['空腹_後'] for s in 種),
           H5c=sum(差(d[('獲得型', s)], '後') >= 差(d[('獲得型', s)], '育') / 2 for s in 種))
res['判定'] = {k: res[k] >= 8 for k in ['H5a', 'H5b', 'H5c']}
res['中央値'] = {h: {k: round(float(np.median([r[k] for r in rows if r['頭'] == h])), 3) for k in ['P養_育', 'P他_育', 'P養_後', 'P他_後', '空腹_前', '空腹_後']} for h in ['獲得型', '道具型']}
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
