"""選び.py の数え直し：手 x ごとに P(a=x | 視線=x) − P(a=x | 視線≠x)（持ち上がり）を、端の手／真ん中の手で平均。手の好き嫌いの偏りを打ち消す。"""
import numpy as np
from multiprocessing import Pool
import importlib.util
_sp = importlib.util.spec_from_file_location('S115選び', '../S115_Qが視線を覚えない理由_20261119/選び.py'); S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)
def one(job):
    s, lr, 直, Qだけ = job; S.設定['Qだけ'] = Qだけ; S.B.換算, S.C.直 = S.窓換算, S.窓直
    try: o = S.C.一生(s, 4, '本物', 学び率=lr, 視線直=直)
    finally: S.B.換算, S.C.直 = S.原換算, S.原直
    A, 相, 視 = o['行動列'], o['相手列'], o['視線列']; 好 = np.array(o['好み']); 順 = np.argsort(好); 端 = {int(順[0]), int(順[-1])}
    上 = {True: [], False: []}
    for i in range(8):
        m = np.arange(7000, 8000)[相[7000:8000, i] == 0]; g = 視[m, 0]; a = A[m, i]
        for x in range(4):
            if (g == x).any() and (g != x).any(): 上[x in 端].append((a[g == x] == x).mean() - (a[g != x] == x).mean())
    return np.mean(上[True]), np.mean(上[False])
if __name__ == '__main__':
    with Pool(8) as p:
        for 直 in [False, True]:
            for lr in [0.01, 0.05, 0.2]:
                out = [np.median(np.array(p.map(one, [(s, lr, 直, Q) for s in range(900, 910)])), 0) for Q in [False, True]]
                print(f'直={直} lr={lr}: 持ち上がり そのまま 端{out[0][0]:+.3f} 真ん中{out[0][1]:+.3f} | Qだけ 端{out[1][0]:+.3f} 真ん中{out[1][1]:+.3f}')
