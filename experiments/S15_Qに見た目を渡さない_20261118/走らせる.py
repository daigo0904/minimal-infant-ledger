import sys, json, numpy as np
sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118')
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
原 = W.赤ちゃん
def 定数だけ(φ):
    z = np.zeros_like(φ); z[-1] = φ[-1]; return z
class 見た目なし(原):
    """Q には定数（最後の1）だけを渡す。評価の予測・つながりには見た目を渡す"""
    def 選ぶ(self, φ):
        q = self.Q @ 定数だけ(φ); ê = np.array([m.予測(φ) for m in self.評価]); score = q + W.重み * self.つながり.予測(φ) * ê
        a = int(np.argmax(score))
        if self.手.random() < W.探る: a = int(self.手.integers(W.行動数))
        return a, q, ê
    def 受ける(self, φ, a, q, e, 食べた, 我慢=0.0):
        super().受ける(φ, a, q, e, 食べた, 我慢)
        φ2, a2, R = self.前; self.前 = (定数だけ(φ2), a2, R)   # 次の手の Q の更新は定数だけで
def 一生(s, 腕, 寿命=8000):
    W.赤ちゃん = 原 if 腕 == '普通' else 見た目なし
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命)
    finally: W.赤ちゃん = 原
if sys.argv[1] == '確かめ':
    import importlib.util
    sp = importlib.util.spec_from_file_location('元', '../S2d_Qの歩幅を直す_20261118/世界.py'); 元 = importlib.util.module_from_spec(sp); sp.loader.exec_module(元); 元.感覚数 = 256; 元.見た目雑音 = 0.3
    a = 一生(5599, '普通', 800); b = 一生(5599, '見た目なし', 800); c = 元.一生(5599, '依存', '獲得型', 寿命=800, 離乳=800)
    print('普通＝S2d:', a['sha256'] == c['sha256'], ' 普通≠見た目なし:', a['sha256'] != b['sha256'], ' 違う手:', int((a['行動列'] != b['行動列']).sum())); sys.exit()
段 = sys.argv[1]; 種 = range(5600, 5610) if 段 == '本' else range(5700, 5710)
def 区(o, lo=7000, hi=8000):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po), float(o['h列'][70:80].mean())]
rows = []
for s in 種:
    r = dict(種=s, 普通=区(一生(s, '普通')), 見た目なし=区(一生(s, '見た目なし'))); rows.append(r); print(r, flush=True)
res = dict(H_漏れが減る=sum(r['見た目なし'][1] < r['普通'][1] for r in rows), H_見られ分けが増える=sum(r['見た目なし'][2] > r['普通'][2] for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(4)] for k in ['普通', '見た目なし']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
