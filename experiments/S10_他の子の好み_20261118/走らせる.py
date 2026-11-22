import sys, json, numpy as np
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
def 区(o, lo=7000, hi=8000):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return float(pa), float(po)
if sys.argv[1] == '確かめ':
    sys.path.insert(0, '../S2d_Qの歩幅を直す_20261118'); import importlib.util
    spec = importlib.util.spec_from_file_location('元', '../S2d_Qの歩幅を直す_20261118/世界.py'); 元 = importlib.util.module_from_spec(spec); spec.loader.exec_module(元); 元.感覚数 = 256; 元.見た目雑音 = 0.3
    a = W.一生(4599, '依存', '獲得型', 寿命=1000, 離乳=1000); b = W.一生(4599, '依存', '獲得型', 寿命=1000, 離乳=1000, 他の子='固定好み'); c = 元.一生(4599, '依存', '獲得型', 寿命=1000, 離乳=1000)
    print('同じ＝元:', a['sha256'] == c['sha256'], ' 同じ≠固定好み:', a['sha256'] != b['sha256']); sys.exit()
段 = sys.argv[1]; 種 = range(4600, 4610) if 段 == '本' else range(4700, 4710)
rows = []
for s in 種:
    r = dict(種=s)
    for 他 in ['同じ', '固定好み']:
        r[他] = 区(W.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 他の子=他))
    rows.append(r); print(s, r, flush=True)
res = dict(H_漏れが減る=sum(r['固定好み'][1] < r['同じ'][1] for r in rows), H_見られ分けが増える=sum(r['固定好み'][0] - r['固定好み'][1] > r['同じ'][0] - r['同じ'][1] for r in rows))
res['判定'] = {k: v >= 8 for k, v in res.items()}
res['中央値'] = {他: dict(P養=round(float(np.median([r[他][0] for r in rows])), 3), P他=round(float(np.median([r[他][1] for r in rows])), 3), 差=round(float(np.median([r[他][0] - r[他][1] for r in rows])), 3)) for 他 in ['同じ', '固定好み']}
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
