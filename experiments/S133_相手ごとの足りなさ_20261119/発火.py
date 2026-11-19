import sys, numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S132共', '../S132_親友がいないと_20261119/共.py')
G = L('S133頭', '../S133_相手ごとの足りなさ_20261119/頭.py')
包 = G.に(C.B.換算, C.W, C.B); 子 = []
class 見る(包):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); 子.append(s); s.番 = i; s.記 = []
    def 選ぶ(s, φ):
        r = super().選ぶ(φ); j, 似 = s.近い(φ); s.記.append((j if 似 > G.設定['しきい'] else -1, s.覚[j][2] if (j is not None and 似 > G.設定['しきい']) else 0.0)); return r
for しきい, 大事, T, 最大 in [(0.85, 0.8, 400.0, 8), (0.85, 0.95, 400.0, 8), (0.8, 0.95, 400.0, 8)]:
    子.clear(); G.設定.update(kD=0.0, しきい=しきい, 大事=大事, T=T, 最大=最大); C.N.赤ちゃん = None
    C.W.学び率 = 0.01; C.B.v時定数 = 5000.0; C.W.見た目次元 = 12; C.N.赤ちゃん = 見る
    o = C.N.一生(900, '依存', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='親友', 親友不在=(7000, 500)); C.W.見た目次元 = 8
    相 = o['相手列']; 
    for c in 子[:3]:
        i = c.番; 記 = np.array(c.記); 養 = 相[:, i] == 0; 友 = 相[:, i] == (i + 1) % 8 + 1; 他 = (相[:, i] > 0) & ~友
        def 主(m): v = 記[m, 0].astype(int); v = v[v >= 0]; return (np.bincount(v, minlength=4) / max(1, len(v))).round(2).tolist(), round(float((記[m, 0] >= 0).mean()), 2)
        print(f'しきい{しきい} 大事{大事} 子{i}: 覚えた数 {len(c.覚)} | 養育者の時 {主(養)} | 親友の時 {主(友)} | 他の仲間の時 {主(他)} | 7500〜7600 親友の時の d {記[7500:7600][友[7500:7600], 1].mean() if 友[7500:7600].any() else -1:.2f}  6800〜7000 {記[6800:7000][友[6800:7000], 1].mean():.2f}')
