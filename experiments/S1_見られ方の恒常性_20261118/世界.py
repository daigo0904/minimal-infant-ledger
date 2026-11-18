"""S1 見られ方の恒常性：養育者1人＋赤ちゃん8人の世界。事前登録.md の値で固定。"""
import hashlib, json
import numpy as np

人数 = 8
行動数 = 4
寿命 = 6000
最後 = 1000
r時定数 = 50.0
育ち時定数 = 2000.0
探る = 0.1
雑音 = 0.2
養育者の好み = [-0.8, -0.2, 0.3, 0.9]
同じ = 0.8
違う = -0.4
忘却 = 0.9995
P初め = 100.0
次元 = 人数 * 行動数 + 2
条件 = ['A', 'A0', 'B', 'B0']


class 予測器:
    """RLS で評価 e を予測する。入力は 見ている相手×行動 の one-hot 32 ＋ 同じ行動 1 ＋ 定数 1。"""

    def __init__(self):
        self.w = np.zeros(次元)
        self.P = np.eye(次元) * P初め

    @staticmethod
    def 入力(相手, 行動, 相手の直前):
        φ = np.zeros(次元)
        φ[相手 * 行動数 + 行動] = 1.0
        if 相手 > 0 and 行動 == 相手の直前:  # 相手 0 は養育者、1..7 は自分以外の赤ちゃん（相対番号）
            φ[人数 * 行動数] = 1.0
        φ[-1] = 1.0
        return φ

    def 予測(self, φ):
        return float(self.w @ φ)

    def 学ぶ(self, φ, e):
        Pφ = self.P @ φ
        k = Pφ / (忘却 + φ @ Pφ)
        self.w += k * (e - self.w @ φ)
        self.P = (self.P - np.outer(k, Pφ)) / 忘却


def 一生(種, 条件名, 生まれつきr=None, 寿命=寿命, 記録=False):
    """1つの世界を1回走らせる。世界の乱数（相手の順番・雑音・最初の行動・好み・r*）は条件によらず同じ。"""
    assert 条件名 in 条件
    世 = np.random.default_rng([種, 0])
    好み = np.array(養育者の好み)[世.permutation(行動数)]
    相手 = np.empty((寿命, 人数), dtype=int)  # 0=養育者、それ以外は赤ちゃんの絶対番号+1
    for t in range(寿命):
        for i in range(人数):
            if 世.random() < 0.5:
                相手[t, i] = 0
            else:
                others = [j for j in range(人数) if j != i]
                相手[t, i] = others[世.integers(人数 - 1)] + 1
    雑 = 世.normal(0, 雑音, (寿命, 人数))
    直前 = 世.integers(行動数, size=人数)
    rstar = np.linspace(-0.6, 0.8, 人数)[世.permutation(人数)] if 生まれつきr is None else np.array(生まれつきr, float)
    if 条件名 in ['B', 'B0']:
        rstar = np.zeros(人数)
    頭 = [予測器() for _ in range(人数)]
    手の乱数 = [np.random.default_rng([種, 1, i]) for i in range(人数)]
    r = np.zeros(人数)
    偏差 = np.zeros((寿命, 人数))
    r列 = np.zeros((寿命, 人数))
    行動列 = np.zeros((寿命, 人数), dtype=int)
    h = hashlib.sha256()
    for t in range(寿命):
        行動 = np.zeros(人数, dtype=int)
        φs = []
        for i in range(人数):
            k = 相手[t, i]
            相対 = 0 if k == 0 else (k - 1) + (1 if k - 1 < i else 0)  # 相手の番号を 1..7 に詰める
            相手の直前 = -1 if k == 0 else int(直前[k - 1])
            候補 = [予測器.入力(相対, a, 相手の直前) for a in range(行動数)]
            乱 = 手の乱数[i]
            if 条件名 in ['A0', 'B0']:
                a = int(乱.integers(行動数))
            else:
                ê = [頭[i].予測(φ) for φ in 候補]
                次 = [r[i] + (x - r[i]) / r時定数 for x in ê]
                a = int(np.argmin([(x - rstar[i]) ** 2 for x in 次]))
                if 乱.random() < 探る:
                    a = int(乱.integers(行動数))
            行動[i] = a
            φs.append(候補[a])
        for i in range(人数):
            k = 相手[t, i]
            if k == 0:
                e = 好み[行動[i]]
            else:
                e = 同じ if 行動[i] == 直前[k - 1] else 違う
            e = float(np.clip(e + 雑[t, i], -1, 1))
            頭[i].学ぶ(φs[i], e)
            r[i] += (e - r[i]) / r時定数
            if 条件名 in ['B', 'B0']:
                rstar[i] += (r[i] - rstar[i]) / 育ち時定数
            偏差[t, i] = (r[i] - rstar[i]) ** 2
        直前 = 行動.copy()
        r列[t] = r
        行動列[t] = 行動
        h.update(行動.tobytes()); h.update(r.tobytes()); h.update(rstar.tobytes())
    from scipy.stats import spearmanr
    平均r = r列[-最後:].mean(axis=0)
    ρ = float(spearmanr(rstar, 平均r).statistic)
    out = dict(種=種, 条件=条件名, D=float(偏差[-最後:].mean()), ρ=ρ, rstar=rstar.tolist(), 最後の平均r=平均r.tolist(),
               好み=好み.tolist(), 行動の割合=np.bincount(行動列[-最後:].ravel(), minlength=行動数).tolist(), sha256=h.hexdigest())
    if 記録:
        out['行動列'] = 行動列
        out['r列'] = r列
        out['相手列'] = 相手
    return out
