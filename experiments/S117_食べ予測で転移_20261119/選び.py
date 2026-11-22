"""調整用の種 900〜909：食べ予測の頭（kf3）で S110 の転移。4000〜5000 の仲間の視線の持ち上がり（端／真ん中）と、養育者の視線を追い続けるか。"""
import numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S117頭', '../S117_食べ予測で転移_20261119/頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
def one(job):
    s, kf, a = job; o = H.一生(s, kf, a, 視線切替=4000)
    仲 = H.持ち上がり(o, 4000, 5000, 相手=1); 仲終 = H.持ち上がり(o, 7000, 8000, 相手=1); 養 = H.持ち上がり(o, 4000, 5000)
    return [np.mean(仲), np.mean(仲終), np.mean(養)]
if __name__ == '__main__':
    with Pool(8) as p:
        for kf in [0.0, 3.0]:
            for a in ['本物', 'ずらし']:
                r = np.array(p.map(one, [(s, kf, a) for s in range(900, 910)])); m = np.median(r, 0)
                print(f'kf={kf} 前半{a}: 仲間の視線 4000-5000 {m[0]:+.3f}  7000-8000 {m[1]:+.3f} | 養育者の視線 4000-5000 {m[2]:+.3f}')
