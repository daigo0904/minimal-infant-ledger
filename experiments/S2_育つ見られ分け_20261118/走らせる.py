import json, sys, numpy as np
from pathlib import Path
import 世界 as W
段 = sys.argv[1]
種 = {'本': range(2000, 2010), '追試': range(2100, 2110)}[段]
Path('結果').mkdir(exist_ok=True); f = Path(f'結果/{段}.json'); assert not f.exists()
rows = []
for s in 種:
    for w in W.世界の種類:
        for h in W.頭の種類:
            o = W.一生(s, w, h); AD, 喜, 差 = W.区間の数字(o)
            rows.append(dict(種=s, 世界=w, 頭=h, 差=差, 喜=喜, AD=AD, sha256=o['sha256'], 空腹=float(o['h列'].mean()), 食=float(o['食列'].mean())))
    print(s, flush=True)
json.dump(dict(段=段, 行=rows), f.open('x'), ensure_ascii=False, indent=1)
