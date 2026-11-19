import numpy as np, importlib.util, itertools
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S = L('S129選び', '../S129_相手に効く欠乏_20261119/選び.py')
def one(job):
    s, kD, 目, 速 = job; S.G.設定['目安'] = 目; S.G.設定['速'] = 速
    try: return S.one((s, kD))
    finally: S.G.設定['目安'] = 0.02; S.G.設定['速'] = 50.0
if __name__ == '__main__':
    with Pool(8) as p:
        for 目, 速, kD in itertools.product([0.05], [200.0, 400.0], [10.0, 30.0]):
            r = np.array(p.map(one, [(s, kD, 目, 速) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'目安={目} 速={速} kD={kD}: 増え {m[0]:+.3f}（>0 {int((r[:,0] > 0).sum())}/10） なしの P養 {m[1]:.3f} 見られ分け {m[2]:.3f}')
