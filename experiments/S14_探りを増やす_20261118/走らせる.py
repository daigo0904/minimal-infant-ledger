import sys, json, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
原 = W.赤ちゃん; 貪 = []
class K(原):
    def 選ぶ(self, φ):   # S2d の 選ぶ と同じ計算。貪欲な行動を記録するだけ
        q = self.Q @ φ; ê = np.array([m.予測(φ) for m in self.評価]); score = q + W.重み * self.つながり.予測(φ) * ê
        a = int(np.argmax(score)); 貪.append(a)
        if self.手.random() < W.探る: a = int(self.手.integers(W.行動数))
        return a, q, ê
def 一生(s, ε, 寿命=8000):
    貪.clear(); W.探る = ε; W.赤ちゃん = K
    try: o = W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原; W.探る = 0.1
    o['貪欲列'] = np.array(貪).reshape(寿命, 8); return o
if sys.argv[1] == '確かめ':
    a = 一生(5399, 0.1, 800); W.探る = 0.1; b = W.一生(5399, '依存', '獲得型', 寿命=800, 離乳=800)
    print('記録つき＝S2d:', a['sha256'] == b['sha256'], ' 0.1≠0.3:', a['sha256'] != 一生(5399, 0.3, 800)['sha256']); sys.exit()
段 = sys.argv[1]; 種 = range(5400, 5410) if 段 == '本' else range(5500, 5510)
def 区(A, 相, b, lo=7000, hi=8000):
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po)]
rows = []
for s in 種:
    r = dict(種=s)
    for ε in [0.1, 0.3]:
        o = 一生(s, ε); r[f'貪{ε}'] = 区(o['貪欲列'], o['相手列'], o['一番']); r[f'実{ε}'] = 区(o['行動列'], o['相手列'], o['一番'])
    rows.append(r); print(r, flush=True)
res = dict(H_漏れが減る=sum(r['貪0.3'][1] < r['貪0.1'][1] for r in rows), H_見られ分けが増える=sum(r['貪0.3'][2] > r['貪0.1'][2] for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(3)] for k in ['貪0.1', '貪0.3', '実0.1', '実0.3']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
