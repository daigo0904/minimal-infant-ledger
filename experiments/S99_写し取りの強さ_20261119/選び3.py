"""調整用の種 900〜909：S95 の作り（4000 で赤ちゃん7 が新入り）で、写す頭の kM ごとに新入りのしきたり率。"""
import numpy as np
from multiprocessing import Pool
from 共通 import *
def one(job):
    s, kM, 型 = job; o = 一生(s, 型, True, kM, 新入り=4000); A = o['行動列'][:, 7]; 相 = o['相手列'][:, 7]; x = しきたりの手(s)
    return (s, kM, 型, float((A[4500:6000] == x).mean()), float((A[4500:6000][相[4500:6000] > 0] == x).mean()), float((A[4500:6000][相[4500:6000] == 0] == x).mean()), float(o['食列'][4500:6000, 7].mean()))
if __name__ == '__main__':
    ks = [0.0, 0.5, 2.0, 5.0]
    with Pool(8) as p: r = p.map(one, [(s, k, 型) for k in ks for 型 in ['でたらめ', '決まった手'] for s in range(900, 910)])
    for k in ks:
        g = lambda 型, j: float(np.median([v[j] for v in r if v[1] == k and v[2] == 型]))
        print(f'kM={k}: 決まった 全体 {g("決まった手",3):.3f} 仲間前 {g("決まった手",4):.3f} 養育者前 {g("決まった手",5):.3f} 食べ {g("決まった手",6):.3f} | でたらめ 全体 {g("でたらめ",3):.3f} 食べ {g("でたらめ",6):.3f}')
