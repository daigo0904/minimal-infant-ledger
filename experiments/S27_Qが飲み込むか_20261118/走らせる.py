import json, sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
from multiprocessing import Pool
W.感覚数 = 256; W.見た目雑音 = 0.3
原 = W.赤ちゃん
記録 = {}
class 記す(原):
    """選ぶ時の Q の手ごとの差（最大−2番目）と つながりの項 重み·u·ê の手ごとの差（最大−最小）を記録するだけ"""
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; 記録[i] = []
    def 選ぶ(s, φ):
        q = np.sort(s.Q @ φ); ê = np.array([m.予測(φ) for m in s.評価]); L = W.重み * s.つながり.予測(φ) * ê
        記録[s.番].append((q[-1] - q[-2], L.max() - L.min())); return super().選ぶ(φ)
def 一生(s, 寿命=8000):
    記録.clear(); W.赤ちゃん = 記す
    try: o = W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原
    return o, np.array([記録[i] for i in range(8)]).transpose(1, 0, 2)   # (手, 子, 2)
def 窓(R, 相, a, b):
    m = 相[a:b] == 0; Qd = np.median(R[a:b, :, 0][m]); Ld = np.median(R[a:b, :, 1][m]); return float(Qd), float(Ld), float(Ld / Qd)
def one(s):
    o, R = 一生(s); 相 = o['相手列']
    return dict(種=s, 初め=窓(R, 相, 0, 500), 育=窓(R, 相, 7000, 8000), 推移=[窓(R, 相, b, b + 500) for b in range(0, 8000, 500)])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        W.赤ちゃん = 原; a = W.一生(8899, '依存', '獲得型', 寿命=600, 離乳=600); b, R = 一生(8899, 寿命=600)
        print('記録しても一生は同じ:', a['sha256'] == b['sha256'], R.shape, '窓(Q差, つながり差, 比):', [round(x, 4) for x in 窓(R, b['相手列'], 0, 500)]); sys.exit(0)
    段 = sys.argv[1]; 種 = range(8800, 8810) if 段 == '本' else range(8900, 8910)
    with Pool(8) as p: rows = p.map(one, list(種))
    res = dict(H1_比が下がる=int(sum(r['初め'][2] > r['育'][2] for r in rows)), H2_Qの差が育つ=int(sum(r['初め'][0] < r['育'][0] for r in rows)))
    res['判定'] = {k: res[k] >= 8 for k in ['H1_比が下がる', 'H2_Qの差が育つ']}
    res['中央値'] = {w: [round(float(np.median([r[w][k] for r in rows])), 4) for k in range(3)] for w in ['初め', '育']}
    res['推移_比'] = [round(float(np.median([r['推移'][k][2] for r in rows])), 3) for k in range(16)]
    res['推移_Q差'] = [round(float(np.median([r['推移'][k][0] for r in rows])), 4) for k in range(16)]
    res['推移_つながり差'] = [round(float(np.median([r['推移'][k][1] for r in rows])), 4) for k in range(16)]
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
