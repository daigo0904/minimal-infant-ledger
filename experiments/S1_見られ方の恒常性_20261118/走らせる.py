"""予備(999)→本(1000..1009)→追試(1100..1109)。各世界で4条件。結果は 結果/<段>.json（上書きしない）。"""
import json, sys, time
from pathlib import Path
import 世界 as W

段 = sys.argv[1]
種 = {'予備': [999], '本': list(range(1000, 1010)), '追試': list(range(1100, 1110))}[段]
out = Path('結果'); out.mkdir(exist_ok=True)
f = out / f'{段}.json'
assert not f.exists(), '上書きしない'
t0 = time.time(); rows = []
for s in 種:
    for c in W.条件:
        rows.append(W.一生(s, c))
    print(s, round(time.time() - t0, 1), flush=True)
with f.open('x') as fp:
    json.dump(dict(段=段, 世界の数=len(種), 行=rows, 秒=time.time() - t0), fp, ensure_ascii=False, indent=1)
