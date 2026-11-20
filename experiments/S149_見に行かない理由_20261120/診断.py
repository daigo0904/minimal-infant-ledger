"""調整用の種 900〜909：S148 の作り・v3 で、物の1手目（t 偶数）の f̂（手ごとの「この手の後 3手以内に食べたか」の予測）を記録。
手がかりなし／あり（良い）／あり（悪い）で、f̂[見る=3]・f̂[取る=0]・他（1,2）の平均。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
sys.path.insert(0, '../S148_分からない時に顔を見る_20261120')
import 共 as C
記 = {}
class 記す(C.包):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; s.t = 0; 記[i] = np.zeros((8000, 4))
    def 選ぶ(s, φ):
        if s.t < 8000: 記[s.番][s.t] = [m.予測(φ) for m in s.食]
        s.t += 1; return super().選ぶ(φ)
def one(s):
    記.clear(); 原 = C.包; C.包 = 記す
    try: o = C.一生(s, '見る', 'v3')
    finally: C.包 = 原
    手, 物 = o['手がかり'], o['物']; out = []
    for 条件 in ['なし', '良い', '悪い']:
        v = []
        for i in range(8):
            t = np.arange(7000, 8000, 2); h = 手[t, i]
            m = (h == 0) if 条件 == 'なし' else (h == (1 if 条件 == '良い' else -1)); F = 記[i][t[m]]
            v.append([F[:, 3].mean(), F[:, 0].mean(), F[:, 1:3].mean()])
        out += list(np.mean(v, 0))
    return out
if __name__ == '__main__':
    with Pool(8) as p: r = np.array(p.map(one, list(range(900, 910))))
    m = np.median(r, 0)
    for k, 条件 in enumerate(['手がかりなし', '手がかりあり（良い）', '手がかりあり（悪い）']):
        print(f'{条件}: f̂[見る] {m[3*k]:.4f}  f̂[取る] {m[3*k+1]:.4f}  f̂[他] {m[3*k+2]:.4f}')
    print('手がかりなしで 見る > 取る の世界:', int((r[:, 0] > r[:, 1]).sum()), '/10   見る（なし）> 見る（良い）:', int((r[:, 0] > r[:, 3]).sum()), '/10')
