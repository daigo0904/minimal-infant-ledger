import sys, json, numpy as np
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
if sys.argv[1] == '確かめ':
    import importlib.util
    sp = importlib.util.spec_from_file_location('元', '../S2d_Qの歩幅を直す_20261118/世界.py'); 元 = importlib.util.module_from_spec(sp); sp.loader.exec_module(元); 元.感覚数 = 256; 元.見た目雑音 = 0.3
    print('S2d と同じ一生:', W.一生(4999, '依存', '獲得型', 寿命=800, 離乳=800)['sha256'] == 元.一生(4999, '依存', '獲得型', 寿命=800, 離乳=800)['sha256']); sys.exit()
段 = sys.argv[1]; 種 = range(5000, 5010) if 段 == '本' else range(5100, 5110)
rows = []
for s in 種:
    o = W.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000); b = o['一番']; A, 相, 食, G = o['行動列'], o['相手列'], o['食列'], o['g列']
    ts = np.arange(4000, 7990)
    後 = np.array([[食[t + 1:t + 6, i].any() for i in range(8)] for t in ts]).ravel()
    a = A[ts].ravel(); w = 相[ts].ravel(); g = G[ts].ravel()
    m = w > 0; a, 後, g = a[m], 後[m], g[m]; best = a == b
    Δ生 = 後[best].mean() - 後[~best].mean()
    edges = np.quantile(g, [0, .2, .4, .6, .8, 1]); idx = np.clip(np.searchsorted(edges, g, side='right') - 1, 0, 4)
    num = den = 0.0
    for k in range(5):
        sel = idx == k
        if (sel & best).sum() and (sel & ~best).sum():
            n = sel.sum(); num += n * (後[sel & best].mean() - 後[sel & ~best].mean()); den += n
    rows.append(dict(種=s, Δ生=float(Δ生), Δg=float(num / den))); print(rows[-1], flush=True)
med = lambda k: round(float(np.median([r[k] for r in rows])), 4)
res = dict(Δ生=med('Δ生'), Δg=med('Δg')); res['判定'] = dict(H_gで消える=abs(res['Δg']) < .01 and res['Δg'] < res['Δ生'] / 2)
print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
