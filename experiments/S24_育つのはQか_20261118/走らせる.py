import json, sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
if sys.argv[1] == '確かめ':
    a = W.一生(8299, '依存', '獲得型', 寿命=800, 離乳=800); b = W.一生(8299, '依存', '道具型', 寿命=800, 離乳=800)
    print('獲得型と道具型で違う一生:', a['sha256'] != b['sha256'], '相手列は同じ:', bool((a['相手列'] == b['相手列']).all())); sys.exit(0)
段 = sys.argv[1]; 種 = range(8200, 8210) if 段 == '本' else range(8300, 8310)
rows = []
for h in ['獲得型', '道具型']:
    for s in 種:
        o = W.一生(s, '依存', h, 寿命=8000, 離乳=8000); _, _, 差 = W.区間の数字(o)
        rows.append(dict(頭=h, 種=s, 初め=差[0], 育=float(np.mean(差[14:16])), 推移=差))
d = {(r['頭'], r['種']): r for r in rows}
gap = {s: (d[('獲得型', s)]['初め'] - d[('道具型', s)]['初め'], d[('獲得型', s)]['育'] - d[('道具型', s)]['育']) for s in 種}
res = dict(H1_差が育つ=sum(g[1] > g[0] for g in gap.values()), H2_道具型も育つ=sum(d[('道具型', s)]['初め'] <= d[('道具型', s)]['育'] / 2 for s in 種))
res['判定'] = {k: res[k] >= 8 for k in ['H1_差が育つ', 'H2_道具型も育つ']}
res['中央値'] = {h: dict(初め=round(float(np.median([r['初め'] for r in rows if r['頭'] == h])), 3), 育った後=round(float(np.median([r['育'] for r in rows if r['頭'] == h])), 3)) for h in ['獲得型', '道具型']}
res['差の中央値'] = dict(初め=round(float(np.median([g[0] for g in gap.values()])), 3), 育った後=round(float(np.median([g[1] for g in gap.values()])), 3))
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
