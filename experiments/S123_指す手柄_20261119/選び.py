"""調整用の種 900〜909：S122 の作り（窓3）で kf=3/10/30、指し効く／効かない。養育者が当たりを見ていない時に当たりを指す割合（指すのが得な場面）と、全体・食べ。"""
import numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S122指頭', '../S122_指さし_20261119/指頭.py'); A2 = L('S122足す2', '../S122_指さし_20261119/足す2.py')
H.食換算 = A2.換算に(H.原換算, H.W, H.B)
def 指す場面(o, lo, hi):
    当 = o['当たり'][0] % 4; 相 = o['相手列'][lo:hi]; A = o['行動列'][lo:hi]; 視 = np.vstack([np.full((1, 8), -1), o['指列'][:-1]])[lo:hi]
    m = (相 == 0) & (視 != 当); n = (相 == 0) & (視 == 当)
    return float((A[m] == 4 + 当).mean()), float((A[n] == 当).mean())
def one(job):
    s, kf, 効 = job; A2.設定['窓'] = 3; A2.設定['kf'] = kf
    try: o = H.一生(s, kf, 効)
    finally: A2.設定['kf'] = 0.0
    return 指す場面(o, 0, 1000) + 指す場面(o, 7000, 8000) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    with Pool(8) as p:
        for kf in [3.0, 10.0, 30.0]:
            for 効 in [True, False]:
                m = np.median(np.array(p.map(one, [(s, kf, 効) for s in range(900, 910)])), 0)
                print(f'kf={kf} 効く={効}: 見ていない時に当たりを指す 初め {m[0]:.3f} 終わり {m[2]:.3f} | 見ている時に当たりを取る 終わり {m[3]:.3f} | 食べ {m[4]:.4f}')
