import json, sys, numpy as np
sys.path.insert(0, '../S2_育つ見られ分け_20261118')
import 世界 as W
rows = []
for s in range(3000, 3010):
    for f in [0.9999, 0.999]:
        W.つながり忘却 = f
        o = W.一生(s, '依存', '獲得型'); AD, 喜, 差 = W.区間の数字(o)
        rows.append(dict(種=s, 忘却=f, 差=差, 喜=喜, sha256=o['sha256']))
育 = lambda r: float(np.mean(r['差'][14:16])); 後 = lambda r: float(np.mean(r['差'][20:24]))
by = {(r['種'], r['忘却']): r for r in rows}; S = range(3000, 3010)
率 = {f: [後(by[(s, f)]) / 育(by[(s, f)]) if 育(by[(s, f)]) > 0 else float('nan') for s in S] for f in [0.9999, 0.999]}
res = dict(H_忘れで決まる=sum(a < b for a, b in zip(率[0.999], 率[0.9999])),
           速い方の育った後0_15以上=sum(育(by[(s, 0.999)]) >= .15 for s in S),
           残り率の中央値={str(f): round(float(np.nanmedian(v)), 3) for f, v in 率.items()},
           育った後の中央値={str(f): round(float(np.median([育(by[(s, f)]) for s in S])), 3) for f in [0.9999, 0.999]},
           離乳後の中央値={str(f): round(float(np.median([後(by[(s, f)]) for s in S])), 3) for f in [0.9999, 0.999]})
res['判定'] = res['H_忘れで決まる'] >= 8
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open('結果.json', 'x'), ensure_ascii=False, indent=1)
