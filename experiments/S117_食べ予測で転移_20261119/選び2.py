import numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S117頭直', '../S117_食べ予測で転移_20261119/頭直.py'); 持 = L('S117頭', '../S117_食べ予測で転移_20261119/頭.py').持ち上がり
def one(job):
    s, 直, a = job; o = H.一生(s, 3.0, a, 直=直, 視線切替=4000)
    return [np.mean(持(o, 3000, 4000)), np.mean(持(o, 3000, 4000, 相手=1)), np.mean(持(o, 4000, 5000, 相手=1)), np.mean(持(o, 7000, 8000, 相手=1)), np.mean(持(o, 4000, 5000))]
if __name__ == '__main__':
    with Pool(8) as p:
        for 直 in [False, True]:
            for a in ['本物', 'ずらし']:
                m = np.median(np.array(p.map(one, [(s, 直, a) for s in range(900, 910)])), 0)
                print(f'kf3 直={直} 前半{a}: 切替前 養{m[0]:+.3f} 仲間{m[1]:+.3f} | 仲間 4000-5000 {m[2]:+.3f} 7000-8000 {m[3]:+.3f} | 養 4000-5000 {m[4]:+.3f}')
