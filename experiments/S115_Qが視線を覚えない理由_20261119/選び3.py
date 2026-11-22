"""調整用の種 900〜909：一生ずっと Qだけ で選ぶ子（癖だけの子）でも視線追いは育たないか。持ち上がりと、視線の手で食べた時の報酬の差（R の差）。"""
import numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S115選び', '../S115_Qが視線を覚えない理由_20261119/選び.py'); S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)
class 一生Q(S.原換算):
    def 選ぶ(s, φ):
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); a = int(np.argmax(q))
        if s.手.random() < S.W.探る: a = int(s.手.integers(S.W.行動数))
        return a, q, ê
def one(job):
    s, lr = job; S.B.換算 = 一生Q
    try: o = S.C.一生(s, 4, '本物', 学び率=lr)
    finally: S.B.換算 = S.原換算
    A, 相, 視, F = o['行動列'], o['相手列'], o['視線列'], o['食列']
    out = []
    for lo, hi in [(0, 1000), (7000, 8000)]:
        上 = []
        for i in range(8):
            m = np.arange(lo, hi)[相[lo:hi, i] == 0]; g = 視[m, 0]; a = A[m, i]
            for x in range(4):
                if (g == x).any() and (g != x).any(): 上.append((a[g == x] == x).mean() - (a[g != x] == x).mean())
        out.append(np.mean(上))
    m = 相 == 0; 合 = (A == 視[:, :1]) & m
    out += [float(F[合].mean()), float(F[m & ~合].mean())]
    return out
if __name__ == '__main__':
    with Pool(8) as p:
        for lr in [0.01, 0.05, 0.2]:
            m = np.median(np.array(p.map(one, [(s, lr) for s in range(900, 910)])), 0)
            print(f'一生Qだけ lr={lr}: 持ち上がり 0-1000 {m[0]:+.3f}  7000-8000 {m[1]:+.3f} | 視線の手で食べ {m[2]:.3f} それ以外 {m[3]:.3f}')
