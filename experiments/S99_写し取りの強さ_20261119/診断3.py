"""調整用の種 900〜909：給餌の形='仲間へ'（切替=0＝見ている子と同じ手なら食べ物）で代替わり。8500〜 全員のしきたり率と「一番多い手」の割合。"""
import numpy as np
from multiprocessing import Pool
from 共通 import *
import 共通
def 一生2(s, 型, kM):
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = H.写す; H.設定['kM'] = kM
    try: return N.一生(s, '依存', '獲得型', 寿命=10000, 離乳=10000, 給餌の形='仲間へ', 切替=0, 食べた見える=True, しきたり=しきたりの手(s) if 型 == '決まった手' else 'でたらめ', しきたり始め=2000, 代替わり=4000, 代替わり間隔=500)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8; H.設定['kM'] = 0.0
def one(job):
    s, 型, kM = job; o = 一生2(s, 型, kM); A = o['行動列']; x = しきたりの手(s); c = np.bincount(A[8500:].ravel(), minlength=K) / A[8500:].size
    return (float((A[8500:] == x).mean()), float(c.max()), float((A[6000:6500] == x).mean()), float(o['食列'][8500:].mean()))
if __name__ == '__main__':
    with Pool(8) as p:
        for kM in [0.0, 2.0]:
            for 型 in ['でたらめ', '決まった手']:
                r = np.array(p.map(one, [(s, 型, kM) for s in range(900, 910)]))
                print(f'kM={kM} {型}: 8500〜しきたり {np.median(r[:,0]):.3f}  一番多い手 {np.median(r[:,1]):.3f}  6000〜6500しきたり {np.median(r[:,2]):.3f}  食べ {np.median(r[:,3]):.3f}  （しきたり>0.3 の世界 {int((r[:,0]>0.3).sum())}/10）')
