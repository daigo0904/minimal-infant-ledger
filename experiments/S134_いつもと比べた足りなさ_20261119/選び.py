"""調整用の種 900〜909：いつもと比べた足りなさ（K=10）で kD=0/10/30/100。S132 の世界（親友不在）と S64 の世界（養育者不在）。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
G = L('S134頭', '../S134_いつもと比べた足りなさ_20261119/頭.py')
C = L('S132共', '../S132_親友がいないと_20261119/共.py'); 包友 = G.に(C.B.換算, C.W, C.B)
R = L('S64R', '../S64_構われないと_20261118/走らせる.py'); 包養 = G.に(R.B.換算, R.W, R.B)
def 友一生(s, 不在, kD):
    G.設定['kD'] = kD; C.W.学び率 = 0.01; C.B.v時定数 = 5000.0; C.W.見た目次元 = 12; C.N.赤ちゃん = 包友
    try: return C.N.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='親友', 親友不在=(7000, 500) if 不在 else None)
    finally: G.設定['kD'] = 0.0; C.W.学び率 = 0.05; C.B.v時定数 = 1000.0; C.W.見た目次元 = 8
def 養一生(s, 腕, kD):
    G.設定['kD'] = kD; 原 = R.B.換算; R.B.換算 = 包養
    try: return R.一生(s, 腕)
    finally: R.B.換算 = 原; G.設定['kD'] = 0.0
def one(job):
    s, kD = job; x, y = C.割(友一生(s, True, kD), 7500, 8000), C.割(友一生(s, False, kD), 7500, 8000)
    b = 養一生(s, 'なし', kD); a = 養一生(s, '欠乏', kD)
    return [x[0] - y[0], R.P養(a, 7500, 7700) - R.P養(b, 7500, 7700), y[0], R.P養(b, 7500, 7700), float(np.mean([R.B.区(b, 7000, 7500)[2], R.B.区(b, 7500, 8000)[2]]))]
if __name__ == '__main__':
    with Pool(8) as p:
        for kD in [0.0, 10.0, 30.0, 100.0]:
            r = np.array(p.map(one, [(s, kD) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'kD={kD}: 親友が戻った増え {m[0]:+.3f}（>0 {int((r[:,0]>0).sum())}/10） 養育者が戻った増え {m[1]:+.3f}（>0 {int((r[:,1]>0).sum())}/10） | 普段 親友 {m[2]:.3f} 養 {m[3]:.3f} 見られ分け {m[4]:.3f}')
