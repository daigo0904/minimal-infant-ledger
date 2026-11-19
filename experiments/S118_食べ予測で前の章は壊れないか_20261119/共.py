import sys, numpy as np, importlib.util
sys.path.insert(0, '../S100_多数に合わせる_20261119')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
A = L('S118足す', '../S118_食べ予測で前の章は壊れないか_20261119/足す.py')
R48 = L('S48R', '../S48_得と邪魔を分ける_20261118/走らせる.py'); S47 = R48.S47
S47.B.換算 = A.換算に(S47.B.換算, S47.W, S47.B); S47.ずらし = A.換算に(S47.ずらし, S47.W, S47.B)
R100 = L('S100R', '../S100_多数に合わせる_20261119/走らせる.py'); 共100 = sys.modules['共通']
共100.H.写す = A.写すに(共100.H.写す, 共100.W, 共100.B, 共100.H.設定)
def 見られ分け(s, 腕, kf, 寿命=8000):
    A.設定['kf'] = kf
    try: o = R48.一生(s, 腕, 寿命)
    finally: A.設定['kf'] = 0.0
    return o, R48.S47.B.区(o, 0, 500)[2], float(np.mean([R48.S47.B.区(o, 7000, 7500)[2], R48.S47.B.区(o, 7500, 8000)[2]]))
def しきたり(s, 多数, 型, kf, 寿命=10000):
    A.設定['kf'] = kf
    try: o = R100.世(s, '流行り', 多数, 型, 寿命)
    finally: A.設定['kf'] = 0.0
    x = R100.しきたりの手(s); return o, float((o['行動列'][8500:] == x).mean()) if 寿命 >= 10000 else None
