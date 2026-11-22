import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S99頭', '../S99_写し取りの強さ_20261119/頭.py')
B, W = H.B, H.W
N = L('S99世界', '../S99_写し取りの強さ_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
K = 16
def しきたりの手(s):
    当 = int(np.random.default_rng([s, 7]).integers(K)); return (当 + 5) % K
def 一生(s, 型, 褒める, kM, 寿命=6000, **kw):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = H.写す; H.設定['kM'] = kM
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, お手本=False, 当たり固定=True, 仲間は褒めない=not 褒める,
                       しきたり=しきたりの手(s) if 型 == '決まった手' else 'でたらめ', **kw)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8; H.設定['kM'] = 0.0
