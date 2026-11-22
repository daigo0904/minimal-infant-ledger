"""Re-run a few stored worlds with their original seeds and check the results match exactly.
Run from the repository root:  python3 analysis/check_reproduce.py
Checks S152 (B0 and v4, all five chapters, seed 32800), S48 (seed 13001) and S41 (seed 11601)
through the frozen confirmatory script of S252. Each job runs in a fresh process, as in the original runs."""
import glob, json, os, sys
from multiprocessing import Pool
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experiments")
S252 = glob.glob(os.path.join(ROOT, "S252_*"))[0]
os.chdir(S252)  # scripts load sibling experiments through ../, so they run from their own folder
sys.path.insert(0, S252)
import 本番テスト as m

def stored(exp):
    return json.load(open(glob.glob(os.path.join(ROOT, exp + "_*", "結果_本.json"))[0]))

if __name__ == "__main__":
    v = stored("S152")["値"]
    jobs = [("S152", 32800, n, w) for n in ["元", "v4"] for w in m.G.世界一覧] + [("S48", 13001, "ずらし"), ("S41", 11601, "道具", "無関係")]
    with Pool(8, maxtasksperchild=1) as p:
        r = p.map(m.job, jobs, chunksize=1)
    ok = 0
    for x in r[:10]:
        i = ["元", "v4"].index(x[2]); k = m.G.世界一覧.index(x[3])
        ok += abs(v[i][k][0] - x[4]) < 1e-12
    s48 = [q[2:] for q in stored("S48")["行"] if q[0] == 13001 and q[1] == "ずらし"][0]
    s41 = [q[3:] for q in stored("S41")["行"] if q[0] == 11601 and q[1] == "道具" and q[2] == "無関係"][0]
    ok += list(s48) == list(r[10][3:]); ok += list(s41) == list(r[11][4:])
    print(f"{ok}/12 values reproduced exactly")
    sys.exit(0 if ok == 12 else 1)
