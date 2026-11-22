import sys, json, numpy as np, importlib.util
def 読む(名, path):
    sp = importlib.util.spec_from_file_location(名, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); m.感覚数 = 256; m.見た目雑音 = 0.3; return m
W = 読む('S16世界', '../S16_気に入りを持ち越さない_20261118/世界.py')
原 = W.赤ちゃん
class 線形(原):
    def 受ける(self, φ, a, q, e, 食べた, 我慢=0.0):
        super().受ける(φ, a, q, e, 食べた, 我慢); φ2, a2, R = self.前; self.前 = (φ2, a2, -self.h)
def 一生(s, 腕, 寿命=8000):
    W.赤ちゃん = 原 if 腕 == '元' else 線形
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='持ち越す' if 腕 == '元' else 'その手だけ')
    finally: W.赤ちゃん = 原
if sys.argv[1] == '確かめ':
    S2d = 読む('S2d', '../S2d_Qの歩幅を直す_20261118/世界.py')
    a = 一生(7099, '元', 600); b = 一生(7099, 'まとめ', 600); c = S2d.一生(7099, '依存', '獲得型', 寿命=600, 離乳=600)
    print('元＝S4の形(S2d・256・0.3):', a['sha256'] == c['sha256'], ' 元≠まとめ:', a['sha256'] != b['sha256']); sys.exit()
段 = sys.argv[1]; 種 = range(7000, 7010) if 段 == '本' else range(7100, 7110)
def 区(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po)]
rows = []
for s in 種:
    r = dict(種=s)
    for 腕 in ['元', 'まとめ']:
        o = 一生(s, 腕); r[腕 + '_初め'] = 区(o, 0, 500); r[腕 + '_育'] = 区(o, 7000, 8000); r[腕 + '_推移'] = [区(o, k, k + 1000)[2] for k in range(0, 8000, 1000)]
    rows.append(r); print(s, round(r['元_育'][2], 3), round(r['まとめ_育'][2], 3), round(r['まとめ_初め'][2], 3), flush=True)
res = dict(H_まとめが大きい=sum(r['まとめ_育'][2] > r['元_育'][2] for r in rows), H_育ちで出る=sum(r['まとめ_初め'][2] <= r['まとめ_育'][2] / 2 for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(3)] for k in ['元_初め', '元_育', 'まとめ_初め', 'まとめ_育']}
res['推移の中央値'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(8)] for k in ['元_推移', 'まとめ_推移']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
