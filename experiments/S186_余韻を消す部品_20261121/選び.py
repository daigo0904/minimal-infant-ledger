"""S186：S185 の世界・記憶0.5 で、v4 から部品を1つずつ戻した腕の余韻（調整の種だけ・切り分け）。"""
import sys, numpy as np
sys.path.insert(0, '../S185_見られ分けの余韻_20261121')
from multiprocessing import Pool
import 共
v4 = dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)
腕 = {'元': {}, 'v4': v4, 'λ1': dict(v4, λ=1.0), 'kf0': dict(v4, kf=0.0), 'kD0': dict(v4, kD=0.0), 'kJ0': dict(v4, kJ=0.0), '損もなし': dict(v4, 損も=False)}
共.構成.update(腕)
def one(job): s, 名 = job; o = 共.一生(s, 名, 記憶=0.5); return 共.余韻(o, 7000, 8000) + (o['sha256'],)
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名 in 腕:
            r = p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1); x = np.array([v[:4] for v in r]); m = np.median(x, 0)
            print(f'{名}: 余韻 {m[0]:+.3f}（>0 {int((x[:,0]>0).sum())}/10） 直後 {m[1]:.3f} 続き {m[2]:.3f} 見られ分け {m[3]:+.3f}  sha先頭 {r[0][4][:8]}', flush=True)
