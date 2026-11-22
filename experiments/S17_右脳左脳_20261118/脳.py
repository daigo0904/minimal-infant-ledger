"""S17 右脳・左脳。どの腕も感覚の数は 128（＋定数1）にそろえる。出力（Q・評価の予測・つながり）は左右で共有。"""
import sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.見た目雑音 = 0.3; W.感覚数 = 128
原 = W.赤ちゃん
腕の種類 = ['一つ128', '一つ128体', '役割', '見方', '脳梁なし', '脳梁あり']
腕 = '一つ128'
def 層(rng, n, d):
    return rng.normal(0, 1 / np.sqrt(d), (n, d)), rng.uniform(-0.5, 0.5, n)
class 赤ちゃん(原):
    def __init__(self, 種, i, 頭):
        super().__init__(種, i, 頭)
        rng = np.random.default_rng([種, 6, i]); self.腕 = 腕
        self.直前 = np.zeros(7)   # 体：空腹・直前に食べたか・直前の評価・直前の行動(4)
        if 腕 == '一つ128':   self.A = 層(rng, 128, 8)
        if 腕 == '一つ128体': self.A = 層(rng, 128, 15)
        if 腕 == '役割':      self.R = 層(rng, 64, 8); self.L = 層(rng, 64, 7)
        if 腕 == '見方':      self.R = 層(rng, 64, 8); self.L = 層(rng, 64, 8)
        if 腕 in ('脳梁なし', '脳梁あり'):
            self.R = 層(rng, 64, 8); self.L = 層(rng, 64, 8); self.C = rng.normal(0, 1 / np.sqrt(64), (64, 64))
        self.感覚 = self._感じる
    def _感じる(self, v):
        t = lambda P, x: np.tanh(P[0] @ x + P[1])
        if self.腕 == '一つ128':   z = t(self.A, v)
        elif self.腕 == '一つ128体': z = t(self.A, np.r_[v, self.直前])
        elif self.腕 == '役割':    z = np.r_[t(self.R, v), t(self.L, self.直前)]
        elif self.腕 == '見方':    z = np.r_[t(self.R, np.sign(v)), t(self.L, v)]   # 右＝ざっくり（符号だけ）・左＝細かく
        elif self.腕 == '脳梁なし': z = np.r_[t(self.R, v), t(self.L, v)]
        else:
            l = t(self.L, v); r = np.tanh(self.R[0] @ v + self.R[1] + self.C @ l); z = np.r_[r, l]   # 右は左の出力も受け取る
        return np.append(z, 1.0)
    def 受ける(self, φ, a, q, e, 食べた, 我慢=0.0):
        super().受ける(φ, a, q, e, 食べた, 我慢)
        self.直前 = np.r_[self.h, 1.0 if 食べた else 0.0, e, np.eye(4)[a]]
def 一生(s, 腕名, 寿命=8000):
    global 腕
    腕 = 腕名; W.赤ちゃん = 赤ちゃん
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原
