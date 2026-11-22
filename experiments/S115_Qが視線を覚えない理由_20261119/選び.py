"""調整用の種 900〜909：S109 の作り（本物・手4）で、Q 学び率 × 視線を直に足す か で、7000〜8000 の窓だけ Qだけ にした時の視線追い（端の手／真ん中の手）。"""
import sys, numpy as np
sys.path.insert(0, '../S111_視線を直に_20261119')
from multiprocessing import Pool
import 共通2 as C
B, W = C.B, C.W
設定 = dict(Qだけ=False)
def 窓つき(基):
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.手数 = 0
        def 選ぶ(s, φ):
            t = s.手数; s.手数 += 1
            if not (設定['Qだけ'] and 7000 <= t < 8000): return super().選ぶ(φ)
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); a = int(np.argmax(q))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
    return K
原換算, 原直 = B.換算, C.直
窓換算, 窓直 = 窓つき(原換算), 窓つき(原直)
def one(job):
    s, lr, 直, Qだけ = job; 設定['Qだけ'] = Qだけ; B.換算, C.直 = 窓換算, 窓直
    try: o = C.一生(s, 4, '本物', 学び率=lr, 視線直=直)
    finally: B.換算, C.直 = 原換算, 原直
    A, 相, 視 = o['行動列'], o['相手列'], o['視線列']; 好 = np.array(o['好み']); 順 = np.argsort(好); 端 = {int(順[0]), int(順[-1])}
    r = []
    for i in range(8):
        m = np.arange(7000, 8000)[相[7000:8000, i] == 0]; g = 視[m, 0]; e = np.array([x in 端 for x in g]); 追 = A[m, i] == g
        r.append((追[e].mean(), 追[~e].mean()))
    return np.mean(r, 0)
if __name__ == '__main__':
    with Pool(8) as p:
        for 直 in [False, True]:
            for lr in [0.01, 0.05, 0.2]:
                out = []
                for Qだけ in [False, True]:
                    m = np.median(np.array(p.map(one, [(s, lr, 直, Qだけ) for s in range(900, 910)])), 0); out.append(m)
                print(f'直={直} lr={lr}: そのまま 端{out[0][0]:.3f} 真ん中{out[0][1]:.3f} | Qだけ 端{out[1][0]:.3f} 真ん中{out[1][1]:.3f}')
