import json, sys, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
from multiprocessing import Pool
W.感覚数 = 256; W.見た目雑音 = 0.3
原 = W.赤ちゃん
記録 = {}
class 記す(原):
    """選ぶ時のつながり u を毎手記録するだけ（行動は変えない）"""
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; 記録[i] = []
    def 選ぶ(s, φ):
        記録[s.番].append(s.つながり.予測(φ)); return super().選ぶ(φ)
def 一生(s, 寿命=8000):
    記録.clear(); W.赤ちゃん = 記す
    try: o = W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原
    U = np.array([記録[i] for i in range(8)]).T; return o, U
def 窓(U, 相, a, b):
    養 = np.mean([U[a:b, i][相[a:b, i] == 0].mean() for i in range(8)]); 他 = np.mean([U[a:b, i][相[a:b, i] > 0].mean() for i in range(8)]); return 養, 他
def one(s):
    o, U = 一生(s); 相 = o['相手列']
    初 = 窓(U, 相, 0, 500); 育 = 窓(U, 相, 7000, 8000)
    推移 = [窓(U, 相, b, b + 500) for b in range(0, 8000, 500)]
    return dict(種=s, 初め養=float(初[0]), 初め他=float(初[1]), 育養=float(育[0]), 育他=float(育[1]), 推移=[[float(x) for x in p] for p in 推移])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        W.赤ちゃん = 原; a = W.一生(8699, '依存', '獲得型', 寿命=600, 離乳=600); b, U = 一生(8699, 寿命=600)
        print('記録しても一生は同じ:', a['sha256'] == b['sha256'], '記録の形:', U.shape, 'u が0でない:', bool(np.abs(U[-1]).max() > 0), '窓:', [round(x, 4) for x in 窓(U, b['相手列'], 0, 500)]); sys.exit(0)
    段 = sys.argv[1]; 種 = range(8600, 8610) if 段 == '本' else range(8700, 8710)
    with Pool(8) as p: rows = p.map(one, list(種))
    res = dict(H1_出すぎ=int(sum(r['初め養'] > r['育養'] for r in rows)), H2_見分けも縮む=int(sum(r['初め養'] - r['初め他'] > r['育養'] - r['育他'] for r in rows)))
    res['判定'] = {k: res[k] >= 8 for k in ['H1_出すぎ', 'H2_見分けも縮む']}
    med = lambda k: round(float(np.median([r[k] for r in rows])), 4)
    res['中央値'] = {k: med(k) for k in ['初め養', '初め他', '育養', '育他']}
    res['推移_養'] = [round(float(np.median([r['推移'][k][0] for r in rows])), 4) for k in range(16)]
    res['推移_他'] = [round(float(np.median([r['推移'][k][1] for r in rows])), 4) for k in range(16)]
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
