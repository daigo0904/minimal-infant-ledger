import sys, numpy as np
sys.path.insert(0, '../S158_損を重く見る_20261120')
from multiprocessing import Pool
from 共 import *
腕 = {'ずっと1.0': (1, 1.0), '1.0→0.5': (1, 1.0, 0.5, 4000), 'ずっと0.5': (1, 0.5), '0.5→1.0': (1, 0.5, 1.0, 4000)}
def one(job): s, 名, w = job; o = 一生(s, '養育者', 物知り=腕[名], 記録=True, 損重さ=w); return 数える(o, s, 腕[名], 6000, 8000) + (float(o['食列'][6000:].mean()),)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for w in [1.0, 2.0, 3.0]:
            r = {名: np.array(p.map(one, [(s, 名, w) for s in range(900, 910)], chunksize=1)) for 名 in 腕}; f = lambda 名: r[名][:, 1]
            失 = f('ずっと1.0') - f('1.0→0.5'); 得 = f('0.5→1.0') - f('ずっと0.5')
            print(f'損重さ{w}: ' + ' '.join(f'{名} {np.median(f(名)):+.3f}' for 名 in 腕) + f' ／ 失う量 {np.median(失):.3f} 育つ量 {np.median(得):.3f} 失う>育つ {int((失 > 得).sum())}/10 食べ(ずっと1.0) {np.median(r["ずっと1.0"][:, 5]):.4f}', flush=True)
