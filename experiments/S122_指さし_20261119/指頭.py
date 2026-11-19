"""S122：食べ予測（kf=3）の換算型で指さしの世界。手8（0〜3取る・4〜7指す）。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S122共通2', '../S122_指さし_20261119/共通2.py')
A = L('S118足す', '../S118_食べ予測で前の章は壊れないか_20261119/足す.py')
B, W, N = C.B, C.W, C.N
原換算 = B.換算; 食換算 = A.換算に(原換算, W, B)
def 一生(s, kf, 効く, 寿命=8000):
    A.設定['kf'] = kf; B.換算 = 食換算
    W.学び率 = 0.01; B.v時定数 = 5000.0; K = 8; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 4; W.見た目次元 = 8 + K + 1 + K; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True, 視線=True, 当たり固定=True, 指さし=True, 指し効く=効く)
    finally: A.設定['kf'] = 0.0; B.換算 = 原換算; W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def 数える(o, lo, hi):
    A, 相 = o['行動列'][lo:hi], o['相手列'][lo:hi]; 当 = o['当たり'][0] % 4; 養 = 相 == 0
    指当 = float((A[養] == 4 + 当).mean()); 指 = float((A[養] >= 4).mean())
    # 指した次の手（養育者がまだ見ていれば）当たりを取る割合
    続, n = 0, 0
    for i in range(8):
        for t in range(lo, hi - 1):
            if o['相手列'][t, i] == 0 and o['行動列'][t, i] == 4 + 当 and o['相手列'][t + 1, i] == 0: n += 1; 続 += int(o['行動列'][t + 1, i] == 当)
    return 指当, 指, (続 / n if n else float('nan')), float(o['食列'][lo:hi].mean())
