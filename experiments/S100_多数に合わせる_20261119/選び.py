"""調整用の種 900〜909：代替わりの作りで、写す（見た手）／多数（見た手の頻度の一番）× 世界（流行り＝しきたりは損／仲間へ＝合わせると得）。"""
import sys, numpy as np, itertools
from multiprocessing import Pool
from 共通 import *
代 = dict(しきたり始め=2000, 代替わり=4000, 代替わり間隔=500)
def one(job):
    s, 形, 多数, kM, 型 = job; kw = dict(代, 切替=0) if 形 == '仲間へ' else dict(代)
    o = 一生(s, 型, True, kM, 寿命=10000, 多数=多数, 形=形, **kw); A = o['行動列']; x = しきたりの手(s)
    return float((A[8500:] == x).mean()), float((A[6500:7000] == x).mean())
if __name__ == '__main__':
    C = [(形, 多数, kM) for 形 in sys.argv[1:] or ['仲間へ', '流行り'] for 多数, kM in [(False, 2.0), (True, 2.0), (True, 5.0)]]
    with Pool(8) as p:
        for 形, 多数, kM in C:
            r = {型: np.array(p.map(one, [(s, 形, 多数, kM, 型) for s in range(900, 910)])) for 型 in ['でたらめ', '決まった手']}
            print(f'{形} 多数={多数} kM={kM}: 8500〜しきたり 決まった {np.median(r["決まった手"][:,0]):.3f} でたらめ {np.median(r["でたらめ"][:,0]):.3f}（>0.3: {int((r["決まった手"][:,0]>0.3).sum())}/10） 6500〜7000 決まった {np.median(r["決まった手"][:,1]):.3f}')
