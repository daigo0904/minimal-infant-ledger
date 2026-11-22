import numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S120食頭', '../S120_視線で当たりを早く_20261119/食頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
def one(job):
    s, kf, 腕, 直 = job; o = H.一生(s, kf, 腕, 直=直)
    return H.乗り換え(o, 相手=0), H.乗り換え(o, 相手=1), H.乗り換え(o, 窓=1000), float(o['食列'][2000:].mean())
if __name__ == '__main__':
    with Pool(8) as p:
        for kf, 直 in [(0.0, True), (3.0, True), (3.0, False)]:
            for 腕 in ['見える', 'ずらし', '見えない']:
                m = np.median(np.array(p.map(one, [(s, kf, 腕, 直) for s in range(900, 910)])), 0)
                print(f'kf={kf} 直={直} {腕}: 切替後200手 当たり 養育者前 {m[0]:.3f} 仲間前 {m[1]:.3f} | 1000手 {m[2]:.3f} | 食べ {m[3]:.4f}')
