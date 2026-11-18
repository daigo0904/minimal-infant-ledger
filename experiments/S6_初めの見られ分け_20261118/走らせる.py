import json, sys, numpy as np
from collections import deque
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
原 = W.赤ちゃん
ずらし幅 = 1000
class ずらし(原):
    """つながりの学びに渡す『食べた』だけを1000手前のものにする（行動・空腹・Q には本物を使う）"""
    def __init__(s, *a):
        super().__init__(*a); s.昔 = deque([False] * 1000, maxlen=1000)
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        偽 = s.昔[0] if ずらし幅 else 食べた; s.昔.append(食べた)
        return s._受ける(φ, a, q, e, 食べた, 偽, 我慢)
    def _受ける(s, φ, a, q, e, 本物, 偽, 我慢):
        before = s.h
        s.h = float(np.clip(before + W.代謝 + 我慢 - (W.一食 if 本物 else 0.0), 0, 1))
        R = -s.h ** 2
        if s.前 is not None:
            φp, ap, Rp = s.前; δ = Rp + W.割引 * q[a] - s.Q[ap] @ φp; s.Q[ap] += W.学び率 * δ * φp / (φp @ φp)
        s.前 = (φ, a, R)
        s.評価[a].学ぶ(φ, e)
        s.r += (e - s.r) / W.r時定数
        s.待ち.append(φ * e); s.食窓.append(1.0 if 偽 else 0.0)
        if len(s.待ち) == W.窓:
            ψ = s.待ち.popleft(); y = max(s.食窓); 基準 = s.平均食 if s.窓の数 > 0 else y
            s.つながり.学ぶ(ψ, y - 基準); s.窓の数 += 1; s.平均食 += (y - s.平均食) / min(s.窓の数, W.相関時定数); s.食窓.popleft()
if sys.argv[1] == '確かめ':
    # ずらし幅0なら元の獲得型と同じ一生になるか（作りの確かめ）
    ずらし幅 = 0; W.赤ちゃん = 原; a = W.一生(3599, '依存', '獲得型', 寿命=1500, 離乳=1500); W.赤ちゃん = ずらし; b = W.一生(3599, '依存', '獲得型', 寿命=1500, 離乳=1500)
    print('幅0で同じ一生:', a['sha256'] == b['sha256']); ずらし幅 = 1000; c = W.一生(3599, '依存', '獲得型', 寿命=1500, 離乳=1500); print('幅1000で違う一生:', a['sha256'] != c['sha256']); sys.exit(0)
段 = sys.argv[1]; 種 = range(3500, 3510) if 段 == '本' else range(3600, 3610)
rows = []
for name, cls, h in [('獲得型', 原, '獲得型'), ('ずらし型', ずらし, '獲得型'), ('道具型', 原, '道具型')]:
    W.赤ちゃん = cls
    for s in 種:
        o = W.一生(s, '依存', h, 寿命=8000, 離乳=8000)
        _, _, 差 = W.区間の数字(o); _, _, 差100 = W.区間の数字(dict(行動列=o['行動列'][:2000], 相手列=o['相手列'][:2000], 一番=o['一番']), 区=100)
        rows.append(dict(頭=name, 種=s, 初め=差[0], 育=float(np.mean(差[14:16])), 推移=差100))
W.赤ちゃん = 原
d = {(r['頭'], r['種']): r for r in rows}
res = dict(H_揺れで正=sum(d[('ずらし型', s)]['初め'] >= .03 for s in 種), H_学習の分=sum(d[('獲得型', s)]['育'] > d[('ずらし型', s)]['育'] for s in 種))
res['判定'] = {k: res[k] >= 8 for k in ['H_揺れで正', 'H_学習の分']}
res['中央値'] = {n: dict(初め=round(float(np.median([r['初め'] for r in rows if r['頭'] == n])), 3), 育った後=round(float(np.median([r['育'] for r in rows if r['頭'] == n])), 3),
                       推移=[round(float(np.median([r['推移'][k] for r in rows if r['頭'] == n])), 3) for k in range(20)]) for n in ['獲得型', 'ずらし型', '道具型']}
print(json.dumps(res, ensure_ascii=False, indent=1)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
