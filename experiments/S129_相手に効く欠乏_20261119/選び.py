"""調整用の種 900〜909：S64 の作りに相手に効く欠乏 kD=0/1/3/10。戻った直後 7500〜7700 の P養 の増え（欠乏−なし）と、なしの見られ分け（7000〜8000）。"""
import numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
G = L('S129頭', '../S129_相手に効く欠乏_20261119/頭.py')
R = L('S64R', '../S64_構われないと_20261118/走らせる.py'); 包 = G.に(R.B.換算, R.W, R.B)
def 一生(s, 腕, kD):
    G.設定['kD'] = kD; 原 = R.B.換算; R.B.換算 = 包
    try: return R.一生(s, 腕)
    finally: R.B.換算 = 原; G.設定['kD'] = 0.0
def one(job):
    s, kD = job; a = 一生(s, '欠乏', kD); b = 一生(s, 'なし', kD)
    見 = float(np.mean([R.B.区(b, 7000, 7500)[2], R.B.区(b, 7500, 8000)[2]]))
    return [R.P養(a, 7500, 7700) - R.P養(b, 7500, 7700), R.P養(b, 7500, 7700), 見, float(b['食列'][7000:].mean())]
if __name__ == '__main__':
    with Pool(8) as p:
        for kD in [0.0, 1.0, 3.0, 10.0]:
            r = np.array(p.map(one, [(s, kD) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'kD={kD}: 戻った直後の増え {m[0]:+.3f}（>0 {int((r[:,0] > 0).sum())}/10） なしの P養 {m[1]:.3f} 見られ分け {m[2]:.3f} 食べ {m[3]:.4f}')
