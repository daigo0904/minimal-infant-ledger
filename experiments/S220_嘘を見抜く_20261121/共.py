"""S175：S47 の『本物』と同じ設定（S30 の換算型・学び率0.01・v時定数5000・その手だけ）で、世界を S175 の写しに、頭を S151 の v2（v4）に。"""
import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S220B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S220世界', P + 'S220_嘘を見抜く_20261121/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
V = L('S220v2', P + 'S220_嘘を見抜く_20261121/v2.py'); 包 = V.に(B.換算, W, B)
構成 = {'元': dict(), 'v4': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)}
def 一生(s, 名='元', 寿命=8000, 二人=None, B同じ=False, なぐさめ=False, kE=0.0, 共感型='減り', 泣き=0.0, 代価=0.0, 感謝=None, 寄る=0.0, 困寄る=0.0, 転入=None, 親切=1.0, 親切組=(), 選び替え=None, 同類=0.0, 評判=0.0, 観客入力=False, 見られ評判=False, 見せ組=(), 私的=False, 噂=0.0, 嘘つき=None, 信用=False):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False, kE=kE); V.設定.update(構成[名])
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = 包; N.なぐさめ = なぐさめ; N.なぐさめW = W; N.共感型 = 共感型; N.泣き = 泣き; N.代価 = 代価; N.感謝 = 感謝; N.寄る = 寄る; N.困寄る = 困寄る; N.転入 = 転入; N.親切 = 親切; N.親切組 = 親切組; N.選び替え = 選び替え; N.同類 = 同類; N.評判 = 評判; N.観客入力 = 観客入力; N.見られ評判 = 見られ評判; N.見せ組 = 見せ組; N.私的 = 私的; N.噂 = 噂; N.嘘つき = 嘘つき; N.信用 = 信用
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 二人=二人, B同じ=B同じ)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 分け(o, lo, hi):
    """人ごとの見られ分け：A の前で A好き手の割合 − B の前で A好き手の割合、と B好き手の逆向き、の平均（子の平均）。"""
    A, 相, a1, b1 = o['行動列'][lo:hi], o['相手列'][lo:hi], o['一番'], o['一番B']; r = []
    for i in range(A.shape[1]):
        x, w = A[:, i], 相[:, i]; pA = np.bincount(x[w == 0], minlength=4) / max(1, (w == 0).sum()); pB = np.bincount(x[w == 9], minlength=4) / max(1, (w == 9).sum())
        r.append(((pA[a1] - pB[a1]) + (pB[b1] - pA[b1])) / 2)
    return float(np.mean(r))
def なぐさめ方(o, lo, hi):
    """仲間に見られている手で、相手の空腹が その世界の中央値より上（困っている）／下 の時の 手3 の割合（子の平均）、と困っている相手の空腹の平均。"""
    A, H = o['行動列'][lo:hi], o['相h列'][lo:hi]; m = ~np.isnan(H); 中 = np.median(H[m]); r = []
    for i in range(A.shape[1]):
        a, h = A[:, i], H[:, i]; 困 = h > 中; 平 = (h <= 中) & ~np.isnan(h)
        r.append(((a[困] == 3).mean(), (a[平] == 3).mean()))
    x = np.mean(r, 0); return float(x[0] - x[1]), float(x[0]), float(x[1]), float(np.mean(H[m]))
def 泣きなぐさめ(o, lo, hi, 境=0.5):
    """相手の空腹が 境 より上（泣いている）／以下 の時の 手3 の割合の差（子の平均）、泣いている手の割合、相手の空腹の 90% 点と中央値。"""
    A, H = o['行動列'][lo:hi], o['相h列'][lo:hi]; m = ~np.isnan(H); r = []
    for i in range(A.shape[1]):
        a, h = A[:, i], H[:, i]; 泣 = h > 境; 平 = (h <= 境) & ~np.isnan(h)
        r.append(((a[泣] == 3).mean() if 泣.any() else np.nan, (a[平] == 3).mean()))
    x = np.nanmean(r, 0); return float(x[0] - x[1]), float(x[0]), float(x[1]), float((H[m] > 境).mean()), float(np.percentile(H[m], 90)), float(np.median(H[m]))
