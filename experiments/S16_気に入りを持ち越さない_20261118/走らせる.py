import sys, json, numpy as np
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
if sys.argv[1] == '確かめ':
    import importlib.util
    sp = importlib.util.spec_from_file_location('元', '../S2d_Qの歩幅を直す_20261118/世界.py'); 元 = importlib.util.module_from_spec(sp); sp.loader.exec_module(元); 元.感覚数 = 256; 元.見た目雑音 = 0.3
    a = W.一生(5799, '依存', '獲得型', 寿命=800, 離乳=800); b = W.一生(5799, '依存', '獲得型', 寿命=800, 離乳=800, 給餌の形='その手だけ'); c = 元.一生(5799, '依存', '獲得型', 寿命=800, 離乳=800)
    print('持ち越す＝S2d:', a['sha256'] == c['sha256'], ' 腕が違う:', a['sha256'] != b['sha256'], ' 違う手:', int((a['行動列'] != b['行動列']).sum())); sys.exit()
段 = sys.argv[1]; 種 = range(5800, 5810) if 段 == '本' else range(5900, 5910)
def 区(o, lo=7000, hi=8000):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po), float(o['食列'][:8000].mean())]
rows = []
for s in 種:
    r = dict(種=s, 持ち越す=区(W.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000)), その手だけ=区(W.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='その手だけ'))); rows.append(r); print(r, flush=True)
res = dict(H_漏れが減る=sum(r['その手だけ'][1] < r['持ち越す'][1] for r in rows), H_見られ分けが増える=sum(r['その手だけ'][2] > r['持ち越す'][2] for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値'] = {k: [round(float(np.median([r[k][j] for r in rows])), 3) for j in range(4)] for k in ['持ち越す', 'その手だけ']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
