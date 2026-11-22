"""S158：損重さ を足す（損も の時、我慢の損に掛ける。1.0 なら S151 と同じ）。
S151：損も を足す。損も=True なら食べ予測の手応えを「この手の後 窓 手以内の（食べた −  我慢／0.3）の合計」にする（外れの損も見る）。False なら S142 と同じ（食べたかの最大）。
S142：切替 を足す。'J満'＝共同注意の喜びを満ちている時だけ（kJ·(1−h)）、'f空'＝食べ予測を空腹の時だけ（kf·h）、'両方'。h＝その子の空腹（0〜1）。
S141：kJ を足す＝共同注意の喜び：世界が 子.共同 を立てた手で、癖の報酬に kJ を足す。
S140：kS を足す＝見てもらう喜び：癖（Q）の報酬に kS·max(e,0)·重さ（重さ＝その相手の大事さ）を足す（食べ物に換算しない）。
S139：kf型 を足す。'普通'（S138 と同じ）／'B'（食べ予測の重みを大事な相手の前で下げる：kf·(1−重さ)）／'C'（食べ予測の手応えに承認も入れる：y＝max(食べた, κ·max(e,0)·重さ)）。
一番の赤ちゃん v2：換算型に3つの部品を足した頭（どれも 0 なら元の換算型と同じ手）。
・食べの予測 f̂[a]（この手の後 窓 手以内に食べたか・手ごとの RLS）：score += kf·(f̂ − 平均)   ← S116・S123
・相手に効く欠乏 d（大事な相手からの評価の 遅い平均 − 速い平均）：ê が一番高い手に kD·d·重さ   ← S129
・癖の重み λ：score の q を λ·q に   ← S127
"""
import numpy as np
from collections import deque
設定 = dict(kf=0.0, 窓=3, kD=0.0, 目安=0.05, 速=400.0, 遅=1000.0, λ=1.0, kf型='普通', κ=1.0, kS=0.0, kJ=0.0, 切替=None, 損も=False, 損重さ=1.0)
def に(基, W, B):
    class V2(基):
        def __init__(s, 種, i, 頭):
            super().__init__(種, i, 頭); n = len(s.Q[0]); s.食 = [W.RLS(n) for _ in range(W.行動数)]; s.待 = deque(); s.速_ = s.遅_ = 0.0; s.始め = True
        def 選ぶ(s, φ):
            S = 設定
            if S['kf'] == 0.0 and S['kD'] == 0.0 and S['λ'] == 1.0: return super().選ぶ(φ)
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
            score = S['λ'] * q + B.c * max(s.v食, 0.0) * u * ê
            重さ = float(np.clip(u / S['目安'], 0, 1))
            if S['kf'] != 0.0: f = np.array([m.予測(φ) for m in s.食]); score = score + S['kf'] * (1.0 - 重さ if S['kf型'] == 'B' else 1.0) * (s.h if S['切替'] in ('f空', '両方') else 1.0) * (f - f.mean())
            if S['kD'] != 0.0: score[int(np.argmax(ê))] += S['kD'] * max(s.遅_ - s.速_, 0.0) * float(np.clip(u / S['目安'], 0, 1))
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            S = 設定; f = 1.0 if 食べた else 0.0
            if S['損も']: f = f - S['損重さ'] * 我慢 / 0.3
            if S['kf型'] == 'C': f = max(f, S['κ'] * max(e, 0.0) * min(max(s.つながり.予測(φ), 0.0) / S['目安'], 1.0))
            for x in s.待: x[2] = (x[2] + f) if S['損も'] else max(x[2], f)
            s.待.append([φ, a, f])
            if len(s.待) == S['窓']: φ0, a0, y = s.待.popleft(); s.食[a0].学ぶ(φ0, y)
            x = min(max(s.つながり.予測(φ), 0.0) / S['目安'], 1.0) * e
            if s.始め: s.速_ = s.遅_ = x; s.始め = False
            s.速_ += (x - s.速_) / S['速']; s.遅_ += (x - s.遅_) / S['遅']
            重 = min(max(s.つながり.予測(φ), 0.0) / S['目安'], 1.0)
            r = super().受ける(φ, a, q, e, 食べた, 我慢)
            if S['kS'] != 0.0: φ_, a_, R_ = s.前; s.前 = (φ_, a_, R_ + S['kS'] * max(e, 0.0) * 重)
            if S['kJ'] != 0.0 and getattr(s, '共同', False): φ_, a_, R_ = s.前; s.前 = (φ_, a_, R_ + S['kJ'] * ((1.0 - s.h) if S['切替'] in ('J満', '両方') else 1.0))
            return r
    V2._v2 = True
    return V2
