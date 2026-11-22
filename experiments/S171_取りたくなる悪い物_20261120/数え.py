"""S170：赤ちゃん1（何でも取る仲間）を除いて、S169 と同じ数え方。"""
import sys, numpy as np
sys.path.insert(0, '../S171_取りたくなる悪い物_20261120')
from 共 import 一生
子ら = [0, 2, 3, 4, 5, 6, 7]
def 別々(o, lo, hi):
    A, 物, 手 = o['行動列'][:, 子ら], o['物'][:, 子ら], o['手がかり'][:, 子ら]; t = np.arange(lo, hi); t = t[t % 2 == 0]; A, 物, 手 = A[t], 物[t], 手[t]; 取 = A == 0; m = 手 == 0
    return float(取[m & (物 == 1)].mean()), float(取[m & (物 == -1)].mean())
def 痛い目(o, 始め=4000, 終わり=4600):
    A, 物 = o['行動列'][始め:, 子ら], o['物'][始め:, 子ら]; 悪取 = (A == 0) & (物 == -1); 初 = []
    for i in range(A.shape[1]):
        w = np.flatnonzero(悪取[:, i]); 初.append(int(w[0]) if len(w) else len(A))
    return float(np.median(初)), float(悪取[:終わり - 始め].sum(0).mean())
def 測る(s, k, 何でも, 似せる=None):
    o = 一生(s, '見る', 'v4', 種類=(4000,), k代理=k, 何でも=何でも, 似せる=似せる); g, b = 別々(o, 4000, 4600); 初, 回 = 痛い目(o)
    return g, b, 初, 回, float(o['食列'][4000:4600][:, 子ら].mean()), o['sha256']
