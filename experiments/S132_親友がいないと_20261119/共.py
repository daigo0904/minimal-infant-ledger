import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S50R', '../S50_相手の直前の手が見える_20261118/走らせる.py'); B, W = R.B, R.W
N = L('S132世界', '../S132_親友がいないと_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
G = L('S129頭', '../S129_相手に効く欠乏_20261119/頭.py'); 包 = G.に(B.換算, W, B)
def 一生(s, 不在, kD, 寿命=8000):
    G.設定.update(目安=0.05, 速=400.0, 遅=1000.0, kD=kD); W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = 包
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='親友', 親友不在=(7000, 500) if 不在 else None)
    finally: G.設定['kD'] = 0.0; W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 割(o, a, b):
    A, 相, 一, 友 = o['行動列'][a:b], o['相手列'][a:b], o['一番'], o['親友の手']
    友見 = lambda i: 相[:, i] == (i + 1) % 8 + 1
    return float(np.mean([(A[友見(i), i] == 友).mean() for i in range(8)])), float(np.mean([(A[相[:, i] == 0, i] == 一).mean() for i in range(8)]))
def one(job):
    s, kD = job; a = 一生(s, True, kD); b = 一生(s, False, kD); x, y = 割(a, 7500, 8000), 割(b, 7500, 8000)
    return [x[0] - y[0], x[1] - y[1], y[0], y[1]]
