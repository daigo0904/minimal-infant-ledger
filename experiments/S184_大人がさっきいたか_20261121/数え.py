"""S180：S152 一覧の '122'（S123 の指さしの世界・頭 S151 v2）の世界だけを S180 の写しに差しかえて読む。数え方は S179 と同じ。"""
import numpy as np, importlib.util
P = '../'
sp = importlib.util.spec_from_file_location('S152一覧', P + 'S152_一番の赤ちゃんv4_20261120/一覧.py'); G = importlib.util.module_from_spec(sp); sp.loader.exec_module(G)
sp = importlib.util.spec_from_file_location('S184世界', P + 'S184_大人がさっきいたか_20261121/世界.py'); N2 = importlib.util.module_from_spec(sp); sp.loader.exec_module(N2); N2.感覚数 = 256; N2.見た目雑音 = 0.3
def 教える(o, lo, hi):
    当 = o['当たり'][0] % 4; 相 = o['相手列'][lo:hi]; A = o['行動列'][lo:hi]; 視 = np.vstack([np.full((1, 8), -1), o['指列'][:-1]])[lo:hi]
    m = (相 == 0) & (視 != 当); n = (相 == 0) & (視 == 当); 指 = A == 4 + 当; 取 = A == 当
    return float(指[m].mean()), float(指[n].mean()), float(取[n].mean()), float(取[m].mean())
def 測る(s, 名, 隠す=False, 漂い=None, 寿命=8000, 差しかえ=True, 記憶=None):
    V, M = G.かける('122'); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False); V.設定.update(G.構成[名]); M.A2.設定['kf'] = 0.0
    if 差しかえ: N2.視線隠す = 隠す; N2.漂い = 漂い; N2.記憶 = 記憶; N2.記憶W = M.H.W; M.H.N = N2
    o = M.H.一生(s, 0.0, True, 寿命=寿命)
    if 寿命 < 8000: return o['sha256']
    a = 教える(o, 0, 1000); b = 教える(o, 7000, 8000)
    return (b[0] - b[1], a[0] - a[1]) + a + b + (float(o['食列'][7000:].mean()), o['sha256'])
def 長く(s, α, 中身='両方', 寿命=24000, 気づく=False):
    V, M = G.かける('122'); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False); V.設定.update(G.構成['v4']); M.A2.設定['kf'] = 0.0
    N2.視線隠す = True; N2.漂い = 'いない時'; N2.記憶 = α; N2.記憶中身 = 中身; N2.気づく = 気づく; N2.記憶W = M.H.W; M.H.N = N2
    o = M.H.一生(s, 0.0, True, 寿命=寿命)
    if 寿命 < 8000: return o['sha256']
    x = 教える(o, 寿命 - 2000, 寿命); return (x[0] - x[1], x[2] - x[3], float(o['食列'][寿命 - 2000:].mean()), o['sha256'])
