import json, sys, numpy as np
段 = sys.argv[1]; v = json.load(open(f'結果/{段}.json'))
d = {(r['種'], r['世界'], r['頭']): r for r in v['行']}; S = sorted({r['種'] for r in v['行']})
初め = lambda r: r['差'][0]; 育 = lambda r: float(np.mean(r['差'][14:16])); 後 = lambda r: float(np.mean(r['差'][20:24])); 喜後 = lambda r: float(np.mean(r['喜'][20:24]))
g = lambda s, w, h: d[(s, w, h)]
c = dict(
 H1=dict(獲得=sum(育(g(s,'依存','獲得型')) >= .15 for s in S), 道具=sum(育(g(s,'依存','道具型')) <= .05 for s in S)),
 H2=sum(初め(g(s,'依存','獲得型')) <= 育(g(s,'依存','獲得型')) / 2 for s in S),
 H3=sum(育(g(s,'無関係','獲得型')) < 育(g(s,'依存','獲得型')) for s in S),
 H4=dict(残る=sum(後(g(s,'依存','獲得型')) >= 育(g(s,'依存','獲得型')) / 2 for s in S), 喜ばせ=sum(喜後(g(s,'依存','獲得型')) > 喜後(g(s,'依存','道具型')) for s in S)))
c['判定'] = dict(H1=c['H1']['獲得'] >= 8 and c['H1']['道具'] >= 8, H2=c['H2'] >= 8, H3=c['H3'] >= 8, H4=c['H4']['残る'] >= 8 and c['H4']['喜ばせ'] >= 8)
c['中央値'] = {f'{w}×{h}': dict(初め=round(float(np.median([初め(g(s,w,h)) for s in S])),3), 育った後=round(float(np.median([育(g(s,w,h)) for s in S])),3), 離乳後=round(float(np.median([後(g(s,w,h)) for s in S])),3), 離乳後の喜ばせ=round(float(np.median([喜後(g(s,w,h)) for s in S])),3)) for w in ['依存','無関係'] for h in ['獲得型','道具型','ランダム']}
print(json.dumps(c, ensure_ascii=False, indent=1)); open(f'結果/判定_{段}.json','w').write(json.dumps(c, ensure_ascii=False, indent=1))
