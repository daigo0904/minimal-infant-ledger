"""S18 左右が別々に学ぶ頭（S17b の 別々 を土台に）。右＝見た目の符号（ざっくり）64、左＝見た目そのまま＋自分の体 64。
止める時刻 以降、止めた側は値を出さず（0）、学びもしない。"""
import sys, numpy as np
sys.path.insert(0, '../S17b_左右が別々に学ぶ_20261118'); sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W, 二つの脳 as T
原 = W.赤ちゃん
設定 = dict(止める=None, 止める時刻=8000)
class 左右(T.二つ):
    def __init__(self, 種, i, 頭):
        super().__init__(種, i, 頭)
        rng = np.random.default_rng([種, 9, i]); self.左.W_ = rng.normal(0, 1 / np.sqrt(15), (64, 15)); self.左.b_ = rng.uniform(-.5, .5, 64)
        self.直前 = np.zeros(7); self.手数 = 0
        self.左.φ = lambda v: np.append(np.tanh(self.左.W_ @ np.r_[v, self.直前] + self.左.b_), 1.0)
    def _止め(self):
        return 設定['止める'] if self.手数 >= 設定['止める時刻'] else None
    def 選ぶ(self, v):
        φR, qR, sR = self._値(self.右, v); φL, qL, sL = self._値(self.左, v); 止 = self._止め()
        s = (0 if 止 == '右' else sR) + (0 if 止 == '左' else sL)
        a = int(np.argmax(s)) if np.ndim(s) else int(self.手.integers(W.行動数))
        if self.手.random() < W.探る: a = int(self.手.integers(W.行動数))
        self._今 = (φR, qR, φL, qL); return a, None, None
    def 受ける(self, v, a, q, e, 食べた, 我慢=0.0):
        φR, qR, φL, qL = self._今; 止 = self._止め()
        if 止 != '右': self.右.学.受ける(φR, a, qR, e, 食べた, 我慢)
        else: self.右.学.h = self.左.学.h   # 止めた側は学ばない（体の値だけ合わせておく）
        if 止 != '左': self.左.学.受ける(φL, a, qL, e, 食べた, 我慢)
        else: self.左.学.h = self.右.学.h
        if 止 == '右': self.右.学.h = self.左.学.h
        self.直前 = np.r_[self.h if 止 != '右' else self.左.学.h, 1.0 if 食べた else 0.0, e, np.eye(4)[a]]; self.手数 += 1
    @property
    def h(self): return self.左.学.h if 設定['止める'] == '右' and self.手数 >= 設定['止める時刻'] else self.右.学.h
def 一生(s, 止める, 寿命=9000, 止める時刻=8000):
    設定.update(止める=止める, 止める時刻=止める時刻); T.設定.update(右の速さ=1.0, 脳梁=True); W.赤ちゃん = 左右
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原; W.感覚数 = 128; 設定.update(止める=None)
