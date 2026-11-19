import numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S125叙頭', '../S125_叙述的指さし_20261119/叙頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
def one(job): s, 叙, kf = job; o = H.一生(s, 叙, kf); return H.指す(o, 0, 1000) + H.指す(o, 7000, 8000)
if __name__ == '__main__':
    with Pool(8) as p:
        for kf in [0.0, 3.0]:
            for 叙 in ['褒める', '褒めない']:
                m = np.median(np.array(p.map(one, [(s, 叙, kf) for s in range(900, 910)])), 0)
                print(f'kf={kf} {叙}: 養育者の前で指す 初め {m[0]:.3f} 終わり {m[3]:.3f} | 仲間の前 終わり {m[4]:.3f} | 食べ 終わり {m[5]:.4f}')
