"""調整用の種 900〜909：S122 の作り（指し効く・窓3・kf3）で、7000〜8000 の養育者が見ている手ごとに f̂（8手）を記録。
養育者が当たりを見ていない時（指すのが得な場面）と見ている時（取るのが得な場面）で、f̂[当たりを指す]・f̂[当たりを取る]・他の手の平均を比べる。"""
import numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S122指頭', '../S122_指さし_20261119/指頭.py'); A2 = L('S122足す2', '../S122_指さし_20261119/足す2.py')
記 = {}
def 記録つき(基):
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; s.t = 0; 記[i] = np.zeros((8000, 8))
        def 選ぶ(s, φ):
            if s.t < 8000: 記[s.番][s.t] = [m.予測(φ) for m in s.食]
            s.t += 1; return super().選ぶ(φ)
    return K
H.食換算 = 記録つき(A2.換算に(H.原換算, H.W, H.B))
def one(s):
    記.clear(); A2.設定['窓'] = 3; A2.設定['kf'] = 3.0
    try: o = H.一生(s, 3.0, True)
    finally: A2.設定['kf'] = 0.0
    当 = o['当たり'][0] % 4; 相 = o['相手列']; 視 = np.vstack([np.full((1, 8), -1), o['指列'][:-1]])   # t の始めの養視
    out = []
    for 見 in [False, True]:
        v = []
        for i in range(8):
            m = np.arange(7000, 8000)[(相[7000:8000, i] == 0) & ((視[7000:8000, i] == 当) == 見)]; F = 記[i][m]
            他 = np.delete(F, [当, 4 + 当], axis=1).mean(1)
            v.append([F[:, 4 + 当].mean(), F[:, 当].mean(), 他.mean()])
        out += list(np.mean(v, 0))
    return out
if __name__ == '__main__':
    with Pool(8) as p: r = np.array(p.map(one, list(range(900, 910))))
    m = np.median(r, 0)
    print(f'養育者が当たりを見ていない時: f̂[当たりを指す] {m[0]:.4f}  f̂[当たりを取る] {m[1]:.4f}  他 {m[2]:.4f}')
    print(f'養育者が当たりを見ている時:   f̂[当たりを指す] {m[3]:.4f}  f̂[当たりを取る] {m[4]:.4f}  他 {m[5]:.4f}')
    print('見ていない時に 指す > 取る の世界:', int((r[:, 0] > r[:, 1]).sum()), '/10   指す > 他:', int((r[:, 0] > r[:, 2]).sum()), '/10')
