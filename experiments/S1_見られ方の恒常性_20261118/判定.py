"""事前登録の線で判定。python 判定.py 本"""
import json, math, sys
段 = sys.argv[1]
v = json.load(open(f'結果/{段}.json'))
by = {}
for r in v['行']:
    by.setdefault(r['種'], {})[r['条件']] = r
n = len(by)
ok = lambda x: (not math.isnan(x)) and x >= 0.7
A効く = sum(w['A']['D'] < w['A0']['D'] for w in by.values())
A追従 = sum(ok(w['A']['ρ']) for w in by.values()); A0追従 = sum(ok(w['A0']['ρ']) for w in by.values())
B効く = sum(w['B']['D'] < w['B0']['D'] for w in by.values())
A比小 = sum(w['A']['D'] / w['A0']['D'] < w['B']['D'] / w['B0']['D'] for w in by.values())
B比小 = sum(w['B']['D'] / w['B0']['D'] < w['A']['D'] / w['A0']['D'] for w in by.values())
線 = 0.8 * n
res = dict(段=段, 世界=n,
           H_A_効く=dict(数=A効く, 判定=A効く >= 線),
           H_A_追従=dict(A=A追従, A0=A0追従, 判定=A追従 >= 線 and A0追従 <= 0.2 * n),
           H_B_効く=dict(数=B効く, 判定=B効く >= 線),
           H_比べ=dict(生まれつきの比が小=A比小, 育ちの比が小=B比小, 判定='生まれつきの方が効く' if A比小 >= 線 else '育ちの方が効く' if B比小 >= 線 else '差なし'),
           世界ごと=[dict(種=s, D={c: round(w[c]['D'], 4) for c in w}, ρ={c: round(w[c]['ρ'], 3) for c in w}) for s, w in sorted(by.items())])
print(json.dumps(res, ensure_ascii=False, indent=1))
open(f'結果/判定_{段}.json', 'w').write(json.dumps(res, ensure_ascii=False, indent=1))
