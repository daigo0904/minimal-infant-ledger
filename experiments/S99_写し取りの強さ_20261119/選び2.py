"""調整用の種 900〜909：承認そのものを報酬に足す頭（k·e を Q の報酬へ）で、新入りの写し取りがどこまで上がるか。"""
import sys, numpy as np, importlib.util, itertools
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S95R', '../S95_意味のないしきたり_20261119/走らせる.py')
k承認 = 0.0
class 承認好き(R.B.換算):
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        super().受ける(φ, a, q, e, 食べた, 我慢); φ_, a_, R_ = s.前; s.前 = (φ_, a_, R_ + k承認 * e)
def one(job):
    global k承認
    s, k, 型 = job; k承認 = k; 原 = R.B.換算; R.B.換算 = 承認好き
    try: o = R.一生(s, 型, True)
    finally: R.B.換算 = 原
    A = o['行動列']; x = R.しきたりの手(s); 相 = o['相手列']
    return (s, k, 型, float((A[4500:6000, 7] == x).mean()), float(o['食列'][4500:6000, 7].mean()), float((A[4500:6000, 7][相[4500:6000, 7] == 0] == o['一番']).mean()))
if __name__ == '__main__':
    ks = [0.0, 0.05, 0.2, 0.5]
    J = [(s, k, 型) for k in ks for 型 in ['でたらめ', '決まった手'] for s in range(900, 910)]
    with Pool(8) as p: r = p.map(one, J)
    for k in ks:
        g = lambda 型, j: float(np.median([v[j] for v in r if v[1] == k and v[2] == 型]))
        print(f'k={k}: しきたり 決まった {g("決まった手",3):.3f} でたらめ {g("でたらめ",3):.3f}  食べ {g("決まった手",4):.3f}  養育者に一番の手 {g("決まった手",5):.3f}')
