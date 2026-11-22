import sys, numpy as np
sys.path.insert(0, '../S116_視線は読めるか_20261119')
from multiprocessing import Pool
import importlib.util
_sp = importlib.util.spec_from_file_location('S116頭', '../S116_視線は読めるか_20261119/頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
def one(job):
    s, kf = job; o = H.一生(s, kf); return H.持ち上がり(o, 0, 1000) + H.持ち上がり(o, 7000, 8000) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    with Pool(8) as p:
        for kf in [0.0, 0.3, 1.0, 3.0]:
            m = np.median(np.array(p.map(one, [(s, kf) for s in range(900, 910)])), 0)
            print(f'kf={kf}: 0-1000 端{m[0]:+.3f} 真ん中{m[1]:+.3f} | 7000-8000 端{m[2]:+.3f} 真ん中{m[3]:+.3f} | 食べ {m[4]:.4f}')
