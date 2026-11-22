"""Tally of preregistered verdicts in S1-S246, as reported in the paper (666 / 424 / 54 / 188 in 217 experiments).
Counts every boolean entry under 結果 -> 判定 that is present in both 結果_本.json and 結果_追試.json.
Run from the repository root: python3 analysis/tally.py"""
import glob, json, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments")
n = both = split = fail = 0; exps = set()
for d in sorted(glob.glob(os.path.join(ROOT, "S*_*"))):
    m = re.match(r"S(\d+)", os.path.basename(d))
    if int(m.group(1)) > 246: continue
    try:
        a = json.load(open(os.path.join(d, "結果_本.json")))["結果"]["判定"]
        b = json.load(open(os.path.join(d, "結果_追試.json")))["結果"]["判定"]
    except (FileNotFoundError, KeyError, TypeError):
        continue
    for k, v in a.items():
        if isinstance(v, bool) and isinstance(b.get(k), bool):
            n += 1; s = v + b[k]; both += s == 2; split += s == 1; fail += s == 0; exps.add(d)
print(f"{n} hypotheses in {len(exps)} experiments: {both} passed both runs, {split} split, {fail} failed both")
