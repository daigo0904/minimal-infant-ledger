import numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S122指頭', '../S122_指さし_20261119/指頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
def one(job):
    s, kf, 効 = job; o = H.一生(s, kf, 効); return H.数える(o, 0, 1000) + H.数える(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for kf in [0.0, 3.0]:
            for 効 in [True, False]:
                m = np.nanmedian(np.array(p.map(one, [(s, kf, 効) for s in range(900, 910)])), 0)
                print(f'kf={kf} 指し効く={効}: 初め 当たりを指す {m[0]:.3f} 指す {m[1]:.3f} | 終わり 当たりを指す {m[4]:.3f} 指す {m[5]:.3f} 指した次に取る {m[6]:.3f} 食べ {m[7]:.4f}  （偶然 当たりを指す 1/8=0.125）')
