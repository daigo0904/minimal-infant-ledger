"""調整用の種 900〜909：S109 の世界（本物・手4）で、養育者が見ている手の φ から「養育者の視線」が線形に読めるか（前半で最小二乗・後半で読み当て）。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S109共通2', '../S109_共同注意_20261119/共通2.py')
集め = {}
class 集める(C.B.換算):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番号 = i; 集め[i] = []
    def 選ぶ(s, φ): 集め[s.番号].append(φ.copy()); return super().選ぶ(φ)
def one(s):
    集め.clear(); 原 = C.B.換算; C.B.換算 = 集める
    try: o = C.一生(s, 4, '本物', 寿命=4000, 学び率=0.01)
    finally: C.B.換算 = 原
    相, 視 = o['相手列'], o['視線列']; 当て = []
    for i in range(8):
        X = np.array(集め[i]); m = 相[:, i] == 0; Xm = X[m]; y = np.eye(4)[視[m, 0]]; h = len(Xm) // 2
        w = np.linalg.lstsq(Xm[:h], y[:h], rcond=None)[0]; 当て.append(float((np.argmax(Xm[h:] @ w, 1) == 視[m, 0][h:]).mean()))
    return float(np.mean(当て))
if __name__ == '__main__':
    with Pool(8) as p: r = p.map(one, list(range(900, 910)))
    print('φ から養育者の視線の読み当て（後半）:', [round(x, 3) for x in r], ' 中央値', round(float(np.median(r)), 3), '（偶然 0.25）')
