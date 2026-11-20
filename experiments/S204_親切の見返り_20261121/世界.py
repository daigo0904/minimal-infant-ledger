"""S204：S203 世界の写し。親切組（最初から共感量を 親切 倍にする子）。
S203：S201 世界の写し。親切（転入生の共感量を倍に）。
S201：S200 世界の写し。転入に (手, 子) の並びを渡せる（何人も順に入れ替える）。
S200：S199 世界の写し。転入（子0 を途中で新しく来た子に入れ替える）。
S199：S196 世界の写し。困寄る（選び直しの重みに γ·相手の空腹 を足す）。
S196：S193 世界の写し。寄る（恩人に見られやすくなる＝一緒にいる相手を恩で選ぶ）。
S193：S190 世界の写し。感謝（恩の記憶・恩人らしさの入力・恩人をなぐさめると共感が増す）。
S190：S189 世界の写し。代価（なぐさめると自分の空腹が進む）。
S189：S188 世界の写し。泣き（毎手その確率で子の空腹が 0.8 に跳ね上がる）。
S188：S175 世界の写し。なぐさめ（見ている仲間の空腹が見え、手3 でその空腹を減らす）。
S175：S16 世界の写し。二人＝割合：養育者の番のその割合を大人B（新しい顔・好みは A の逆）にする。
S2 育つ見られ分け：空腹だけを持って生まれ、養育者の顔と好みと「見られ方の値打ち」を育ちで覚える。

世界：赤ちゃん8人＋養育者1人。毎手、各赤ちゃんを誰か1人が見る（0.5で養育者、残りは他の赤ちゃん）。
赤ちゃんは誰が見ているかを番号では知らない。見えるのは相手の「見た目」（8次元・雑音つき）だけ。
養育者は自分の好みの行動をした赤ちゃんを好きになり（気に入り g）、好きな子ほどよく食べさせる（依存の世界）。
離乳の後、食べ物は好き嫌いと無関係になる。対照の「無関係の世界」では最初から無関係。
"""
import hashlib
なぐさめ = False; なぐさめW = None; 共感型 = '減り'; 泣き = 0.0; 代価 = 0.0; 感謝 = None; 寄る = 0.0; 困寄る = 0.0; 転入 = None; 親切 = 1.0; 親切組 = ()   # S204：最初から 親切 倍にする子の番号。S203：転入生がなぐさめた時の共感量を 親切 倍（転入生だけ kE を上げるのと同じ）。S200：転入＝その手で子0 を新しく来た子に入れ替える（頭は別の種で生まれたて・顔も新しく［種,32］）。S199：困寄る＝γ（相手の空腹にも寄る）。S196：寄る＝β。仲間の番で、誰に見られるかを恩の記憶との似かたで重みづけ（∝exp(β·似)、乱数[種,31]）。S193：感謝＝kG（None なら無し）。恩の記憶（なぐさめてくれた相手の顔・毎手 0.98 倍）と、今の相手との似かた（入力 +1）   # S190：なぐさめ（仲間の前の手3）で自分の空腹が 代価 だけ進む。S189：毎手この確率で子の空腹が 0.8 に跳ね上がる（乱数[種,30]）   # S188：なぐさめ＝True で 見ている仲間の空腹が入力に見え、手3 でその仲間の空腹が 0.05 減る
from collections import deque
import numpy as np

人数 = 8
行動数 = 4
寿命 = 12000
離乳 = 8000
見た目次元 = 8
見た目雑音 = 0.6
評価雑音 = 0.2
養育者の好み = [-0.8, -0.2, 0.3, 0.9]
同じ = 0.8
違う = -0.4
代謝 = 0.01
我慢の代価 = 0.01   # 養育者が一番好む行動は空腹を余計に進める（よい子は疲れる）
一食 = 0.3
気に入り時定数 = 5.0
基本の給餌 = 0.01
気に入りの給餌 = 0.08
無関係の給餌 = 0.05
感覚数 = 64
探る = 0.1
割引 = 0.9
学び率 = 0.05
忘却 = 0.9995
P初め = 10.0
r時定数 = 20.0
相関時定数 = 1000.0
λ時定数 = 3000.0
rstar時定数 = 200.0
重み = 2.0
つながり忘却 = 0.9999
窓 = 5
世界の種類 = ['依存', '無関係']
頭の種類 = ['獲得型', '道具型', 'ランダム']


class 感覚:
    """固定の乱数の層（学ばない）。見た目 → 64個の tanh。"""

    def __init__(self, rng):
        self.W = rng.normal(0, 1 / np.sqrt(見た目次元), (感覚数, 見た目次元))
        self.b = rng.uniform(-0.5, 0.5, 感覚数)

    def __call__(self, v):
        return np.append(np.tanh(self.W @ v + self.b), 1.0)


class RLS:
    def __init__(self, n, 忘れ=None):
        self.w = np.zeros(n)
        self.P = np.eye(n) * P初め
        self.忘れ = 忘却 if 忘れ is None else 忘れ

    def 予測(self, φ):
        return float(self.w @ φ)

    def 学ぶ(self, φ, y):
        Pφ = self.P @ φ
        k = Pφ / (self.忘れ + φ @ Pφ)
        self.w += k * (y - self.w @ φ)
        self.P = (self.P - np.outer(k, Pφ)) / self.忘れ


class 赤ちゃん:
    def __init__(self, 種, i, 頭):
        rng = np.random.default_rng([種, 2, i])
        self.頭 = 頭
        self.感覚 = 感覚(rng)
        self.手 = np.random.default_rng([種, 3, i])
        n = 感覚数 + 1
        self.Q = np.zeros((行動数, n))          # 空腹の値打ち（SARSA・線形）
        self.評価 = [RLS(n) for _ in range(行動数)]  # 見ている相手の評価を予測
        self.h = 0.3
        self.r = 0.0                             # 見られ方
        self.m_f = self.m_r = self.c_fr = 0.0
        self.v_f = self.v_r = 1e-6
        self.λ = 0.0                             # 見られ方の値打ち（育ちで決まる）
        self.rstar = 0.0                         # 見られたい目標（食べる直前5手に受けた評価の平均）
        self.直近 = deque([0.0] * 5, maxlen=5)
        self.前 = None                           # (φ, a, 報酬) を次の手で更新
        self.つながり = RLS(n, つながり忘却)        # この相手に認められると食べられるか（相手の見た目ごと）
        self.待ち = deque()                      # (φ*e) を 窓 手ぶん待つ
        self.食窓 = deque()
        self.平均食 = 0.0
        self.窓の数 = 0

    def 選ぶ(self, φ):
        q = self.Q @ φ
        if self.頭 == 'ランダム':
            return int(self.手.integers(行動数)), q, None
        score = q.copy()
        ê = None
        if self.頭 == '獲得型':
            ê = np.array([m.予測(φ) for m in self.評価])
            score = q + 重み * self.つながり.予測(φ) * ê
        a = int(np.argmax(score))
        if self.手.random() < 探る:
            a = int(self.手.integers(行動数))
        return a, q, ê

    def 受ける(self, φ, a, q, e, 食べた, 我慢=0.0):
        before = self.h
        self.h = float(np.clip(before + 代謝 + 我慢 - (一食 if 食べた else 0.0), 0, 1))
        R = -self.h ** 2                 # 状態の苦しさ（上限で止まっても得にならない）
        if self.前 is not None:  # SARSA：前の手を今の手の Q で更新
            φp, ap, Rp = self.前
            δ = Rp + 割引 * q[a] - self.Q[ap] @ φp
            self.Q[ap] += 学び率 * δ * φp / (φp @ φp)   # 入力の大きさで割る（S2c までは1手の実効歩幅が約0.6で Q が暴れていた）
        self.前 = (φ, a, R)
        self.評価[a].学ぶ(φ, e)
        self.r += (e - self.r) / r時定数
        self.直近.append(e)
        f = 1.0 if 食べた else 0.0
        k = 1 / 相関時定数
        self.m_f += k * (f - self.m_f); self.m_r += k * (self.r - self.m_r)
        self.c_fr += k * ((f - self.m_f) * (self.r - self.m_r) - self.c_fr)
        self.v_f += k * ((f - self.m_f) ** 2 - self.v_f); self.v_r += k * ((self.r - self.m_r) ** 2 - self.v_r)
        相関 = self.c_fr / np.sqrt(self.v_f * self.v_r)
        self.λ += (float(np.clip(相関 * 5, 0, 1)) - self.λ) / λ時定数
        if 食べた:
            self.rstar += (float(np.mean(self.直近)) - self.rstar) / rstar時定数
        self.待ち.append(φ * e); self.食窓.append(f)
        if len(self.待ち) == 窓:
            ψ = self.待ち.popleft()
            y = max(self.食窓)
            基準 = self.平均食 if self.窓の数 > 0 else y
            self.つながり.学ぶ(ψ, y - 基準)
            self.窓の数 += 1
            self.平均食 += (y - self.平均食) / min(self.窓の数, 相関時定数)   # 最初から本当の平均（S2b は0から立ち上がり、初めに偽のつながりが出た）
            self.食窓.popleft()


def 一生(種, 世界, 頭, 寿命=寿命, 離乳=離乳, 給餌の形='持ち越す', 二人=None, B同じ=False):
    assert 世界 in 世界の種類 and 頭 in 頭の種類
    世 = np.random.default_rng([種, 0])
    好み = np.array(養育者の好み)[世.permutation(行動数)]
    一番 = int(np.argmax(好み))
    顔 = 世.normal(0, 1, (人数 + 1, 見た目次元))   # 0=養育者、1..8=赤ちゃん
    相手 = np.zeros((寿命, 人数), dtype=int)
    for t in range(寿命):
        for i in range(人数):
            if 世.random() < 0.5:
                相手[t, i] = 0
            else:
                others = [j for j in range(人数) if j != i]
                相手[t, i] = others[世.integers(人数 - 1)] + 1
    if 二人 is not None:   # S175：大人B（番号 人数+1、好みは A の逆）。養育者の番を 二人 の割合で B に（乱数[種,27]・顔は[種,28]）
        顔 = np.vstack([顔, np.random.default_rng([種, 28]).normal(0, 1, 見た目次元)]); 好みB = 好み.copy() if B同じ else -好み; 一番B = int(np.argmax(好みB))
        換 = np.random.default_rng([種, 27]).random((寿命, 人数)); 相手[(相手 == 0) & (換 < 二人)] = 人数 + 1
    見雑 = 世.normal(0, 見た目雑音, (寿命, 人数, 見た目次元))
    評雑 = 世.normal(0, 評価雑音, (寿命, 人数))
    餌 = 世.random((寿命, 人数))
    直前 = 世.integers(行動数, size=人数)
    if なぐさめ: なぐさめW.見た目次元 += 1 + (1 if 感謝 is not None else 0)   # S188・S193（呼び手が戻す）
    子 = [赤ちゃん(種, i, 頭) for i in range(人数)]
    相h列 = np.full((寿命, 人数), np.nan)
    for kk in 親切組: 子[kk].新入り = True   # S204：親切の印（転入ではない）
    寄乱 = np.random.default_rng([種, 31]).random((寿命, 人数)) if 寄る else None
    if 感謝 is not None:
        for c in 子: c.恩 = np.zeros(見た目次元); c.似 = 0.0
    泣乱 = np.random.default_rng([種, 30]).random((寿命, 人数)) if 泣き else None
    g = np.zeros(人数)
    行動列 = np.zeros((寿命, 人数), dtype=np.int8)
    λ列 = np.zeros((寿命 // 100, 人数)); h列 = np.zeros((寿命 // 100, 人数)); 食列 = np.zeros((寿命, 人数), dtype=bool)
    sha = hashlib.sha256()
    for t in range(寿命):
        φs, 行動, qs = [], np.zeros(人数, dtype=int), []
        if 転入 is not None:   # S200・S201：転入＝手（子0 だけ）または (手, 子) の並び
            for tt, kk in ([(転入, 0)] if isinstance(転入, int) else 転入):
                if t == tt:
                    顔[kk + 1] = np.random.default_rng([種, 32] if kk == 0 else [種, 32, kk]).normal(0, 1, 見た目次元); 子[kk] = 赤ちゃん(種 + 1000003 + kk, kk, 頭); 子[kk].新入り = True   # S203
                    if 感謝 is not None: 子[kk].恩 = np.zeros(見た目次元); 子[kk].似 = 0.0
        if 寄る and 感謝 is not None:   # S196：恩人に寄る（仲間の番だけ）
            for i in range(人数):
                if 0 < 相手[t, i] <= 人数:
                    候 = np.array([j for j in range(人数) if j != i]); w = np.exp(寄る * np.array([float(子[i].恩 @ 顔[j + 1]) / 見た目次元 for j in 候]) + 困寄る * np.array([子[j].h for j in 候])); w = np.cumsum(w / w.sum())   # S199：困寄る
                    相手[t, i] = int(候[min(int(np.searchsorted(w, 寄乱[t, i])), len(候) - 1)]) + 1
        if 泣き:   # S189
            for i in range(人数):
                if 泣乱[t, i] < 泣き: 子[i].h = max(子[i].h, 0.8)
        for i in range(人数):
            見 = 顔[相手[t, i]] + 見雑[t, i]
            if なぐさめ: 見 = np.append(見, 子[相手[t, i] - 1].h if 0 < 相手[t, i] <= 人数 else 0.0)   # S188：見ている仲間の困り具合
            if 感謝 is not None: 似 = float(子[i].恩 @ 顔[相手[t, i]]) / 見た目次元; 子[i].似 = 似; 見 = np.append(見, 似)   # S193：今の相手が恩人らしいか
            φ = 子[i].感覚(見)
            a, q, _ = 子[i].選ぶ(φ)
            φs.append(φ); 行動[i] = a; qs.append(q)
        for i in range(人数):
            k = 相手[t, i]
            if 二人 is not None and k == 人数 + 1:
                e = 好みB[行動[i]]
            elif k == 0:
                e = 好み[行動[i]]
                g[i] += (好み[行動[i]] - g[i]) / 気に入り時定数
            else:
                e = 同じ if 行動[i] == 直前[k - 1] else 違う
            e = float(np.clip(e + 評雑[t, i], -1, 1))
            if 世界 == '依存' and t < 離乳:
                if 給餌の形 == '持ち越す':
                    p = 基本の給餌 + 気に入りの給餌 * max(0.0, g[i])
                else:   # その手だけ：その手に養育者が見て喜んだときだけ上乗せ（他の子の手は基本だけ）。養育者の手は約半分なので上乗せは2倍
                    p = 基本の給餌 + (2 * 気に入りの給餌 * max(0.0, 好み[行動[i]]) if k == 0 else (2 * 気に入りの給餌 * max(0.0, 好みB[行動[i]]) if (二人 is not None and k == 人数 + 1) else 0.0))
            else:
                p = 無関係の給餌
            食べた = bool(餌[t, i] < p)
            疲 = (行動[i] == 一番B) if (二人 is not None and k == 人数 + 1) else (行動[i] == 一番)
            子[i].受ける(φs[i], 行動[i], qs[i], e, 食べた, (我慢の代価 if 疲 else 0.0) + (代価 if (なぐさめ and 行動[i] == 3 and 0 < k <= 人数) else 0.0))   # S190
            食列[t, i] = 食べた
        if なぐさめ:   # S188：手3 をした子は、見ている仲間の空腹を 0.05 減らす（自分の得はなし。子.共感量 に減った分）
            for i in range(人数):
                k = 相手[t, i]; 子[i].共感量 = 0.0
                if 0 < k <= 人数:
                    相h列[t, i] = 子[k - 1].h
                    if 行動[i] == 3:
                        前h = 子[k - 1].h
                        子[k - 1].h = max(0.0, 前h - 0.05)
                        子[i].共感量 = ((前h - 子[k - 1].h) if 共感型 == '減り' else (前h ** 2 - 子[k - 1].h ** 2)) * (1.0 + 感謝 * float(np.clip(子[i].似, 0, 1)) if 感謝 else 1.0)
                        if 親切 != 1.0 and getattr(子[i], '新入り', False): 子[i].共感量 *= 親切   # S203
                        if 感謝 is not None: 子[k - 1].恩 = 子[k - 1].恩 + 顔[i + 1]   # S193：なぐさめられた子は相手の顔を恩に足す   # S188：'苦しさ'＝相手の苦しさ h² の減り（自分の苦しさ −h² と同じ形）
        if 感謝 is not None:
            for c in 子: c.恩 = 0.98 * c.恩   # S193：恩は毎手薄れる
        直前 = 行動.copy()
        行動列[t] = 行動
        if t % 100 == 0:
            λ列[t // 100] = [c.λ for c in 子]; h列[t // 100] = [c.h for c in 子]
        sha.update(行動.tobytes())
    return dict(種=種, 世界=世界, 頭=頭, 行動列=行動列, 相手列=相手, 一番=一番, 相h列=相h列, 一番B=(int(np.argmin(好み)) if 二人 is not None else None),   # 数える用：A が一番嫌う手（B が逆の好みならその一番。B同じでも同じ手を使う）
                好み=好み.tolist(),
                λ列=λ列, h列=h列, 食列=食列, rstar=[c.rstar for c in 子], sha256=sha.hexdigest())


def 区間の数字(out, 区=500):
    """区間ごとの 見られ分け AD と、養育者が見ている時に一番好かれる行動を選んだ割合。"""
    A, 相, 一番 = out['行動列'], out['相手列'], out['一番']
    AD, 喜, 差 = [], [], []
    for b in range(0, len(A), 区):
        d, s, x = [], [], []
        for i in range(A.shape[1]):
            a = A[b:b + 区, i]; who = 相[b:b + 区, i]
            p = np.bincount(a[who == 0], minlength=行動数) / max(1, (who == 0).sum())
            q = np.bincount(a[who > 0], minlength=行動数) / max(1, (who > 0).sum())
            d.append(0.5 * np.abs(p - q).sum()); s.append(p[一番]); x.append(p[一番] - q[一番])
        AD.append(float(np.mean(d))); 喜.append(float(np.mean(s))); 差.append(float(np.mean(x)))
    return AD, 喜, 差
