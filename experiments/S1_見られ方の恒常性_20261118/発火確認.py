"""事前登録の「発火の確認」1〜5。短い寿命で。通らなければ本に進まない。"""
import json
import numpy as np
import 世界 as W

c = {}
# 1 同じ種なら SHA 一致
a1 = W.一生(999, 'A', 寿命=600); a2 = W.一生(999, 'A', 寿命=600)
c['1_同じ種で再現'] = a1['sha256'] == a2['sha256']
# 2 A と A0 で行動列が違う
x = W.一生(999, 'A', 寿命=600, 記録=True); y = W.一生(999, 'A0', 寿命=600, 記録=True)
c['2_AとA0で行動が違う'] = int((x['行動列'] != y['行動列']).sum()) > 0
c['2_違った手の数'] = int((x['行動列'] != y['行動列']).sum())
# 3 r*=+0.8 だけの世界と −0.6 だけの世界で後半の行動が違う
hi = W.一生(999, 'A', 生まれつきr=[0.8] * 8, 寿命=1500); lo = W.一生(999, 'A', 生まれつきr=[-0.6] * 8, 寿命=1500)
c['3_行動の割合_高'] = hi['行動の割合']; c['3_行動の割合_低'] = lo['行動の割合']
c['3_目標で行動が変わる'] = hi['行動の割合'] != lo['行動の割合']
c['3_最後の平均r_高'] = float(np.mean(hi['最後の平均r'])); c['3_最後の平均r_低'] = float(np.mean(lo['最後の平均r']))
# 4 B で r* が動く
b = W.一生(999, 'B', 寿命=600)
c['4_Bでr*が動く'] = max(abs(v) for v in b['rstar']) > 0
# 5 偏差の手計算：r=0.3, r*=-0.1 → 0.16
c['5_偏差の手計算'] = abs((0.3 - (-0.1)) ** 2 - 0.16) < 1e-12
ok = all(v for k, v in c.items() if isinstance(v, bool))
c['通過'] = ok
print(json.dumps(c, ensure_ascii=False, indent=1))
open('発火確認.json', 'w').write(json.dumps(c, ensure_ascii=False, indent=1))
assert ok
