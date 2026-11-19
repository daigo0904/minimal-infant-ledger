import sys, numpy as np
sys.path.insert(0, '../S133_相手ごとの足りなさ_20261119')
from 共 import *
記 = {}
class 記す(包):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; 記[i] = []
    def 選ぶ(s, φ):
        ê = np.array([m.予測(φ) for m in s.評価]); j, 似 = s.近い(φ); d = s.覚[j][2] if (j is not None and 似 > G.設定['しきい']) else 0.0
        記[s.番].append((int(np.argmax(ê)), d, float(np.clip(s.つながり.予測(φ) / 0.05, 0, 1)))); return super().選ぶ(φ)
for s in [900, 901]:
    記.clear(); G.設定.update(kD=30.0, しきい=0.8, 大事=0.95, T=400.0, 最大=8); C.W.学び率 = 0.01; C.B.v時定数 = 5000.0; C.W.見た目次元 = 12; C.N.赤ちゃん = 記す
    o = C.N.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='親友', 親友不在=(7000, 500)); C.W.見た目次元 = 8
    相, 友手, 一 = o['相手列'], o['親友の手'], o['一番']
    for i in range(3):
        X = np.array(記[i]); 友 = 相[:, i] == (i + 1) % 8 + 1; m = 友.copy(); m[:7500] = False
        print(s, i, f'親友の前で ê一番＝親友の手 {np.mean(X[友, 0] == 友手):.2f}  ＝養育者の一番 {np.mean(X[友, 0] == 一):.2f}  戻った後の d {X[m, 1].mean():.2f} 重さ {X[m, 2].mean():.2f}')
