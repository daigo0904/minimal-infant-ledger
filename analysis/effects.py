"""Per-world effect sizes for the paper's headline comparisons: median paired difference,
95% bootstrap interval over worlds (10,000 resamples), and the share of worlds in the predicted direction."""
import glob, json, os, sys
import numpy as np
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments")
def load(e, r):
    p = glob.glob(os.path.join(ROOT, f"{e}_*", f"結果_{r}.json")); assert len(p) == 1, (e, p); return json.load(open(p[0]))
def boot(x, rng):
    x = np.asarray(x, float); b = np.median(rng.choice(x, (10000, len(x))), axis=1)
    return float(np.median(x)), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5)), float(np.mean(x > 0))
def pair(rows, key, a, b, f):
    d = {}
    for x in rows: d.setdefault(x[0], {})[key(x)] = x
    return [f(v[a]) - f(v[b]) for v in d.values() if a in v and b in v]
C = {}
for e in ["S48", "S74"]:
    for r in ["本", "追試"]:
        R = load(e, r)["行"]
        C[(f"{e} B0 − shifted bond (last)", r)] = pair(R, lambda x: x[1], "本物", "ずらし", lambda x: x[3])
        C[(f"{e} B0 − instrumental (last)", r)] = pair(R, lambda x: x[1], "本物", "道具", lambda x: x[3])
for e in ["S129", "S131"]:
    for r in ["本", "追試"]:
        R = load(e, r)["行"]
        C[(f"{e} reunion change, kD30 − B0", r)] = pair(R, lambda x: x[1], 30.0, 0.0, lambda x: x[2] - x[3])
for r in ["本", "追試"]:
    R = load("S130", r)["行"]
    for j, L in [(2, 250), (3, 500), (4, 1000)]:
        C[(f"S130 reunion change after {L} steps (kD30)", r)] = [x[j] for x in R if x[1] == 30.0]
    v = np.array(load("S152", r)["値"])
    names = ["audience", "reunion change", "gaze (mid-pref.)", "imperative pointing", "declarative growth"]
    for k, n in enumerate(names):
        C[(f"S152 v4 − B0: {n}", r)] = list(v[1, k] - v[0, k])
    C[("S152 v4 reunion change (>0)", r)] = list(v[1, 1]); C[("S152 v4 declarative growth (>0)", r)] = list(v[1, 4])
rng = np.random.default_rng(0)
out = {}
for (k, r), x in C.items():
    out.setdefault(k, {})[r] = dict(n=len(x), **dict(zip(["median", "lo", "hi", "share_pos"], [round(t, 3) for t in boot(x, rng)])))
json.dump(out, open("effects.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(f"{k:45s}", "  ".join(f"{r}: {d['median']:+.3f} [{d['lo']:+.3f},{d['hi']:+.3f}] pos {d['share_pos']:.2f} n{d['n']}" for r, d in v.items()))
