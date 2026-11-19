"""調整用の種 900〜909：S64 の作り（7000〜7500 養育者が来ない）に食べ予測 kf=0/1/3 を足して、戻った直後（7500〜7700）の喜ばせ P養 の増え（欠乏 − なし）。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
A = L('S118足す', '../S118_食べ予測で前の章は壊れないか_20261119/足す.py')
R = L('S64R', '../S64_構われないと_20261118/走らせる.py')
R.B.換算 = A.換算に(R.B.換算, R.W, R.B)
def one(job):
    s, kf = job; A.設定['kf'] = kf
    try: a = R.一生(s, '欠乏'); b = R.一生(s, 'なし')
    finally: A.設定['kf'] = 0.0
    return R.P養(a, 7500, 7700) - R.P養(b, 7500, 7700), R.P養(b, 7500, 7700), R.P養(a, 7000, 7500) if False else 0.0
if __name__ == '__main__':
    with Pool(8) as p:
        for kf in [0.0, 1.0, 3.0]:
            r = np.array(p.map(one, [(s, kf) for s in range(900, 910)]))
            print(f'kf={kf}: 増え 中央値 {np.median(r[:,0]):+.3f}（>0 の世界 {int((r[:,0] > 0).sum())}/10）  なしの P養 {np.median(r[:,1]):.3f}')
