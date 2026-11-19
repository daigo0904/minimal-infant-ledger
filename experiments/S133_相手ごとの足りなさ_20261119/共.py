import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S132共', '../S132_親友がいないと_20261119/共.py')
G = L('S133頭', '../S133_相手ごとの足りなさ_20261119/頭.py'); 包 = G.に(C.B.換算, C.W, C.B)
def 一生(s, 不在, kD):
    G.設定.update(kD=kD, しきい=0.8, 大事=0.95, T=400.0, 最大=8, 目安=0.05); C.W.学び率 = 0.01; C.B.v時定数 = 5000.0; C.W.見た目次元 = 12; C.N.赤ちゃん = 包
    try: return C.N.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='親友', 親友不在=(7000, 500) if 不在 else None)
    finally: G.設定['kD'] = 0.0; C.W.学び率 = 0.05; C.B.v時定数 = 1000.0; C.W.見た目次元 = 8
def one(job):
    s, kD = job; a = 一生(s, True, kD); b = 一生(s, False, kD); x, y = C.割(a, 7500, 8000), C.割(b, 7500, 8000)
    return [x[0] - y[0], x[1] - y[1], y[0], y[1]]
