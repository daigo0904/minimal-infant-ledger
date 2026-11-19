"""S117：食べ予測の頭 × 視線を直に足す（S111 の世界と 直 の頭）。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S111共通2', '../S111_視線を直に_20261119/共通2.py')
B, W = C.B, C.W
設定 = dict(kf=0.0)
def 足す(基):
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); n = len(s.Q[0]); s.食 = [W.RLS(n) for _ in range(W.行動数)]
        def 選ぶ(s, φ):
            if 設定['kf'] == 0.0: return super().選ぶ(φ)
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ); f = np.array([m.予測(φ) for m in s.食])
            score = q + B.c * max(s.v食, 0.0) * u * ê + 設定['kf'] * (f - f.mean()); a = int(np.argmax(score))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
            s.食[a].学ぶ(φ, 1.0 if 食べた else 0.0); return super().受ける(φ, a, q, e, 食べた, 我慢)
    return K
原換算, 原直 = B.換算, C.直; 食換算, 食直 = 足す(原換算), 足す(原直)
def 一生(s, kf, 腕='本物', 寿命=8000, 直=False, **kw):
    設定['kf'] = kf; B.換算, C.直 = 食換算, 食直
    try: return C.一生(s, 4, 腕, 寿命=寿命, 学び率=0.01, 視線直=直, **kw)
    finally: B.換算, C.直 = 原換算, 原直; 設定['kf'] = 0.0
