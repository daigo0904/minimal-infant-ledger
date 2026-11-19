import numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S122指頭', '../S122_指さし_20261119/指頭.py'); A2 = L('S122足す2', '../S122_指さし_20261119/足す2.py')
H.食換算 = A2.換算に(H.原換算, H.W, H.B)
def one(job):
    s, 窓, 効 = job; A2.設定['窓'] = 窓; A2.設定['kf'] = 3.0
    o = H.一生(s, 3.0, 効); A2.設定['kf'] = 0.0; return H.数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for 窓 in [1, 2, 3]:
            for 効 in [True, False]:
                m = np.nanmedian(np.array(p.map(one, [(s, 窓, 効) for s in range(900, 910)])), 0)
                print(f'窓={窓} 指し効く={効}: 当たりを指す {m[0]:.3f} 指す {m[1]:.3f} 指した次に取る {m[2]:.3f} 食べ {m[3]:.4f}')
