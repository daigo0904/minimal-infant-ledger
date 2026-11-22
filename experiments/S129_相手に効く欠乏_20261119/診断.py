"""調整用の種 900〜902：kD=3 で、戻った直後 7500〜7700 と普段（6800〜7000）の養育者が見ている手で、d・重さ・「ê が一番高い手＝養育者の一番の手」の割合。欠乏あり／なし。"""
import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S = L('S129選び', '../S129_相手に効く欠乏_20261119/選び.py'); G, R = S.G, S.R
記 = {}
class 記す(S.包):
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; s.t = 0; 記[i] = []
    def 選ぶ(s, φ):
        ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        記[s.番].append((max(s.遅 - s.速, 0.0), float(np.clip(u / G.設定['目安'], 0, 1)), int(np.argmax(ê)), u)); s.t += 1; return super().選ぶ(φ)
for s in [900, 901, 902]:
    for 腕 in ['なし', '欠乏']:
        記.clear(); G.設定['kD'] = 3.0; 原 = R.B.換算; R.B.換算 = 記す
        try: o = R.一生(s, 腕)
        finally: R.B.換算 = 原; G.設定['kD'] = 0.0
        相 = o['相手列']; 一 = o['一番']
        for lo, hi in [(6800, 7000), (7000, 7500), (7500, 7700)]:
            X = [記[i][t] for i in range(8) for t in range(lo, hi) if 相[t, i] == 0]
            Y = [記[i][t] for i in range(8) for t in range(lo, hi) if 相[t, i] > 0]
            if X: X = np.array(X); print(s, 腕, f'{lo}-{hi} 養育者の前: d {X[:,0].mean():.3f} 重さ {X[:,1].mean():.3f} ê一番=養育者の一番 {np.mean(X[:,2] == 一):.3f} u {X[:,3].mean():+.4f}', end=' | ')
            Y = np.array(Y); print(f'仲間の前: d {Y[:,0].mean():.3f} 重さ {Y[:,1].mean():.3f} u {Y[:,3].mean():+.4f}')
