import sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
import 感覚 as S
W.見た目雑音 = 0.3
原 = W.赤ちゃん
感覚の種類 = '育つ'
class 赤ちゃん(原):
    def __init__(self, 種, i, 頭):
        W.感覚数 = S.K
        super().__init__(種, i, 頭)
        self.感覚 = S.型の感覚(np.random.default_rng([種, 5, i]), 感覚の種類 == '育つ')
def 一生(種, 頭, 種類, **kw):
    global 感覚の種類
    感覚の種類 = 種類; W.赤ちゃん = 赤ちゃん
    try: return W.一生(種, '依存', 頭, **kw)
    finally: W.赤ちゃん = 原
