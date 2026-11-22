"""調整用の種 900〜909：一生 Qだけ の子に、食べた手の報酬に k を足す（食べること自体が嬉しい）。k=0/0.3/1 で視線追いが育つか。"""
import numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S115選び3', '../S115_Qが視線を覚えない理由_20261119/選び3.py'); T = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(T)
S = T.S; 設定 = dict(k=0.0)
class 食べ好き(T.一生Q):
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        super().受ける(φ, a, q, e, 食べた, 我慢); φ_, a_, R_ = s.前; s.前 = (φ_, a_, R_ + 設定['k'] * (1.0 if 食べた else 0.0))
def one(job):
    s, k, lr = job; 設定['k'] = k; S.B.換算 = 食べ好き
    try: o = S.C.一生(s, 4, '本物', 学び率=lr)
    finally: S.B.換算 = S.原換算
    A, 相, 視 = o['行動列'], o['相手列'], o['視線列']; 上 = []
    for i in range(8):
        m = np.arange(7000, 8000)[相[7000:8000, i] == 0]; g = 視[m, 0]; a = A[m, i]
        for x in range(4):
            if (g == x).any() and (g != x).any(): 上.append((a[g == x] == x).mean() - (a[g != x] == x).mean())
    return float(np.mean(上)), float(o['食列'][7000:].mean())
if __name__ == '__main__':
    with Pool(8) as p:
        for lr in [0.01, 0.05]:
            for k in [0.0, 0.3, 1.0]:
                m = np.median(np.array(p.map(one, [(s, k, lr) for s in range(900, 910)])), 0)
                print(f'lr={lr} k={k}: 持ち上がり 7000-8000 {m[0]:+.3f}  食べ {m[1]:.4f}')
