"""S134：足りなさを「その相手のいつもと比べて」にする。覚えた相手ごとに会った間の長い平均 ḡ を持ち、d＝max(d·減り, clip((間/ḡ − 1)/K, 0, 1))。
S133 相手ごとの足りなさ：大事な相手（重さ＝clip(u/目安,0,1) が 0.5 超）の見た目 φ を「覚えた相手」（最大4人・見た目の平均）にまとめ、
それぞれに最後に会った時刻と足りなさ d を持つ。会った時、前に会ってからの間 gap で d＝max(d·減り, min(gap/T,1))。
選び：今の相手に一番似た覚えた相手（似ている度 > しきい）の d を、ê が一番高い手にだけ kD·d 足す。kD=0 なら元の換算型と同じ手。"""
import numpy as np
設定 = dict(kD=0.0, 目安=0.05, T=200.0, 減り=0.97, しきい=0.8, 最大=8, 大事=0.95, K=10.0, α=0.05)
def に(基, W, B):
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.覚 = []; s.t = 0   # 覚：[見た目, 最後, d]
        def 近い(s, φ):
            if not s.覚: return None, 0.0
            x = φ / np.linalg.norm(φ); 似 = [float(x @ m[0] / np.linalg.norm(m[0])) for m in s.覚]; j = int(np.argmax(似)); return j, 似[j]
        def 選ぶ(s, φ):
            s.t += 1; u = s.つながり.予測(φ); 重さ = float(np.clip(u / 設定['目安'], 0, 1)); j, 似 = s.近い(φ)
            if 重さ > 設定['大事']:   # 大事な相手に会った
                if j is not None and 似 > 設定['しきい']:
                    m = s.覚[j]; gap = s.t - m[1]
                    if m[3] is None: m[3] = float(gap)
                    m[2] = max(m[2] * 設定['減り'], float(np.clip((gap / m[3] - 1.0) / 設定['K'], 0, 1))); m[3] += 設定['α'] * (gap - m[3]); m[1] = s.t; m[0] = 0.95 * m[0] + 0.05 * φ
                elif len(s.覚) < 設定['最大']: s.覚.append([φ.copy(), s.t, 0.0, None]); j, 似 = len(s.覚) - 1, 1.0
            if 設定['kD'] == 0.0: return super().選ぶ(φ)
            q = s.Q @ φ; ê = np.array([mm.予測(φ) for mm in s.評価])
            score = q + B.c * max(s.v食, 0.0) * u * ê
            if j is not None and 似 > 設定['しきい']: score[int(np.argmax(ê))] += 設定['kD'] * s.覚[j][2] * 重さ
            a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
    return K
