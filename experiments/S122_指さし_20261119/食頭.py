"""S120：食べ予測（S117 頭直と同じ）を S120 の世界で。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S122共通2', '../S122_指さし_20261119/共通2.py')
A = L('S118足す', '../S118_食べ予測で前の章は壊れないか_20261119/足す.py')
B, W, N = C.B, C.W, C.N
原換算, 原直 = B.換算, C.直; 食換算, 食直 = A.換算に(原換算, W, B), A.換算に(原直, W, B)
def 一生(s, kf, 腕, 寿命=8000, 直=True):
    """腕：見える（養育者の視線＝当たり）／ずらし（視線は見えるが乱数）／見えない"""
    A.設定['kf'] = kf; B.換算, C.直 = 食換算, 食直
    W.学び率 = 0.01; B.v時定数 = 5000.0; K = 4; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; 見え = 腕 != '見えない'
    W.見た目次元 = 8 + K + 1 + (K if (見え and not 直) else 0); N.赤ちゃん = C.直 if (直 and 見え) else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, 視線=見え, 視線直=直 and 見え, 視線は当たり=(腕 == '見える'))
    finally: A.設定['kf'] = 0.0; B.換算, C.直 = 原換算, 原直; W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; W.見た目次元 = 8
def 乗り換え(o, 窓=200, 相手=None):
    A, 相 = o['行動列'], o['相手列']; 当 = np.array(o['当たり']); r = []
    for t in range(2000, len(A), 1000):
        a, w = A[t:t + 窓], 相[t:t + 窓]; m = np.ones_like(a, bool) if 相手 is None else ((w == 0) if 相手 == 0 else (w > 0))
        r.append(float((a[m] == 当[t // 1000]).mean()))
    return float(np.mean(r))
