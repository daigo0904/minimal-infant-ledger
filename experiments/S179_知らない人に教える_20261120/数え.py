"""S179：S152 一覧の '122'（S123 の指さしの世界・頭は S151 の v2）をそのまま読む。養育者が見ている手で、
養育者の視線が当たりでない（知らない）時 と 当たりである（知っている）時に、当たりを指す割合。"""
import numpy as np, importlib.util
P = '../'
sp = importlib.util.spec_from_file_location('S152一覧', P + 'S152_一番の赤ちゃんv4_20261120/一覧.py'); G = importlib.util.module_from_spec(sp); sp.loader.exec_module(G)
def 教える(o, lo, hi):
    当 = o['当たり'][0] % 4; 相 = o['相手列'][lo:hi]; A = o['行動列'][lo:hi]; 視 = np.vstack([np.full((1, 8), -1), o['指列'][:-1]])[lo:hi]
    m = (相 == 0) & (視 != 当); n = (相 == 0) & (視 == 当); 指 = A == 4 + 当; 取 = A == 当
    return float(指[m].mean()), float(指[n].mean()), float(取[n].mean()), float(取[m].mean())
def 測る(s, 名):
    V, M = G.かける('122'); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False); V.設定.update(G.構成[名]); M.A2.設定['kf'] = 0.0
    o = M.H.一生(s, 0.0, True); a = 教える(o, 0, 1000); b = 教える(o, 7000, 8000)
    return (b[0] - b[1], a[0] - a[1]) + a + b + (o['sha256'],)   # 終わりの 指す差（知らない−知っている）, 初めの差, 初め4つ, 終わり4つ
