"""S17b 左右が別々に学ぶ頭。左右それぞれが S2d の獲得型の学び手（Q・評価の予測・つながり）を丸ごと持つ。
体（空腹）は同じ入力で左右とも同じに動く。行動は 脳梁あり＝左右の値の和で選ぶ／脳梁なし＝毎手どちらか片方がランダムに選ぶ。"""
import sys, numpy as np
sys.path.insert(0, '../S17_右脳左脳_20261118'); sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W, 脳 as B
原 = W.赤ちゃん
設定 = dict(右の速さ=1.0, 脳梁=True)
class 半分:
    def __init__(self, 種, i, 側):
        W.感覚数 = 64
        self.学 = 原(種, i, '獲得型'); W.感覚数 = 128
        rng = np.random.default_rng([種, 7, i, 側]); self.W_ = rng.normal(0, 1 / np.sqrt(8), (64, 8)); self.b_ = rng.uniform(-.5, .5, 64)
        self.側 = 側
    def φ(self, v):
        x = np.sign(v) if self.側 == 0 else v   # 右＝ざっくり（符号）・左＝細かく
        return np.append(np.tanh(self.W_ @ x + self.b_), 1.0)
class 二つ:
    def __init__(self, 種, i, 頭):
        self.右 = 半分(種, i, 0); self.左 = 半分(種, i, 1); self.手 = np.random.default_rng([種, 8, i])
        速 = 設定['右の速さ']
        if 速 != 1.0:
            for m in self.右.学.評価: m.忘れ = 0.999
            self.右.学.つながり.忘れ = 0.999
        self.感覚 = lambda v: v
    @property
    def h(self): return self.右.学.h
    @property
    def λ(self): return self.右.学.λ
    @property
    def rstar(self): return self.右.学.rstar
    def _値(self, 半, v):
        φ = 半.φ(v); q = 半.学.Q @ φ; ê = np.array([m.予測(φ) for m in 半.学.評価]); return φ, q, q + W.重み * 半.学.つながり.予測(φ) * ê
    def 選ぶ(self, v):
        φR, qR, sR = self._値(self.右, v); φL, qL, sL = self._値(self.左, v)
        if 設定['脳梁']: s = sR + sL
        else: s = sR if self.手.random() < 0.5 else sL
        a = int(np.argmax(s))
        if self.手.random() < W.探る: a = int(self.手.integers(W.行動数))
        self._今 = (φR, qR, φL, qL); return a, None, None
    def 受ける(self, v, a, q, e, 食べた, 我慢=0.0):
        φR, qR, φL, qL = self._今; 元の率 = W.学び率
        W.学び率 = 元の率 * 設定['右の速さ']
        try: self.右.学.受ける(φR, a, qR, e, 食べた, 我慢)
        finally: W.学び率 = 元の率
        self.左.学.受ける(φL, a, qL, e, 食べた, 我慢)
def 一生(s, 腕, 寿命=8000):
    if 腕 in ('共有128', '共有見方'):
        return B.一生(s, {'共有128': '一つ128', '共有見方': '見方'}[腕], 寿命)
    設定['右の速さ'] = 3.0 if 腕 == '別々・右が速い' else 1.0; 設定['脳梁'] = 腕 != '別々・脳梁なし'
    W.赤ちゃん = 二つ
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原; W.感覚数 = 128; 設定.update(右の速さ=1.0, 脳梁=True)
腕の種類 = ['共有128', '共有見方', '別々', '別々・右が速い', '別々・脳梁なし']
