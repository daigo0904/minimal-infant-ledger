import json, sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
段 = sys.argv[1]; 種 = range(2900, 2910) if 段 == '本' else range(2950, 2960)
腕 = {'基本': (64, 0.6), '感覚256': (256, 0.6), '雑音0.3': (64, 0.3), '両方': (256, 0.3)}
rows = []
for name, (n, σ) in 腕.items():
    W.感覚数 = n; W.見た目雑音 = σ
    for h in ['獲得型', '道具型']:
        for s in 種:
            o = W.一生(s, '依存', h, 寿命=8000, 離乳=8000)
            A, 相, b = o['行動列'][7000:8000], o['相手列'][7000:8000], o['一番']
            P養 = float(np.mean([(A[:, i][相[:, i] == 0] == b).mean() for i in range(8)])); P他 = float(np.mean([(A[:, i][相[:, i] > 0] == b).mean() for i in range(8)]))
            rows.append(dict(腕=name, 頭=h, 種=s, P養=P養, P他=P他, 差=P養 - P他))
d = {(r['腕'], r['頭'], r['種']): r['差'] for r in rows}
med = lambda a, h, k: round(float(np.median([r[k] for r in rows if r['腕'] == a and r['頭'] == h])), 3)
res = {f'{a}×{h}': {k: med(a, h, k) for k in ['P養', 'P他', '差']} for a in 腕 for h in ['獲得型', '道具型']}
for h in ['獲得型', '道具型']:
    n = sum(d[('両方', h, s)] > d[('基本', h, s)] for s in 種); up = res[f'両方×{h}']['差'] - res[f'基本×{h}']['差']
    res[f'H_見分け_{h}'] = dict(両方が上=n, 中央値の増え=round(up, 3), 判定=n >= 8 and up >= .05)
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
