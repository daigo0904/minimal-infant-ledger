# S252 confirmatory test on frozen code (no component changed). Re-uses S48, S41 and S152 code unchanged, new seeds.
import sys, os, json, numpy as np, importlib.util
from multiprocessing import Pool
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def mod(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(R, rel)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S48 = mod('S48', 'S48_得と邪魔を分ける_20261118/走らせる.py')
S41 = mod('S41', 'S41_上乗せの対照_20261118/走らせる.py')
G = mod('S152一覧', 'S152_一番の赤ちゃんv4_20261120/一覧.py')
SEEDS = {'本': range(80000, 80030), '追試': range(80100, 80130)}
def job(j):
    k = j[0]
    if k == 'S48': return ('S48',) + S48.one(j[1:])
    if k == 'S41': return ('S41',) + S41.one(j[1:])
    return ('S152',) + tuple(j[1:]) + (G.one(j[1:]),)
def boot(x, n=10000, rng=np.random.default_rng(0)):
    x = np.asarray(x, float); b = np.median(rng.choice(x, (n, len(x))), axis=1)
    return [round(float(np.median(x)), 3), round(float(np.percentile(b, 2.5)), 3), round(float(np.percentile(b, 97.5)), 3)]
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(SEEDS[段])
    jobs = [('S48', s, a) for a in ['本物', 'ずらし', '道具'] for s in S] + [('S41', s, h, w) for h, w in S41.腕 for s in S] + \
           [('S152', s, 名, w) for 名 in ['元', 'v4'] for w in G.世界一覧 for s in S]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(job, jobs, chunksize=1)
    a = {(x[1], x[2]): (x[3], x[4]) for x in r if x[0] == 'S48'}
    b = {(x[1], x[2], x[3]): (x[4], x[5]) for x in r if x[0] == 'S41'}
    c = {(x[1], x[2], x[3]): x[4] for x in r if x[0] == 'S152'}
    上 = lambda s, w, k: b[(s, '換算', w)][k] - b[(s, '道具', w)][k]
    W = G.世界一覧
    d = {
      'C1_B0>shifted': [a[(s, '本物')][1] - a[(s, 'ずらし')][1] for s in S],
      'C2_B0>instrumental': [a[(s, '本物')][1] - a[(s, '道具')][1] for s in S],
      'C3_growth_B0>instrumental': [(a[(s, '本物')][1] - a[(s, '本物')][0]) - (a[(s, '道具')][1] - a[(s, '道具')][0]) for s in S],
      'C4_B0_dependent>unrelated': [b[(s, '換算', '依存')][1] - b[(s, '換算', '無関係')][1] for s in S],
      'C5_addon_dependent>unrelated': [上(s, '依存', 1) - 上(s, '無関係', 1) for s in S],
      'C6_v4_audience>=B0-0.03': [c[(s, 'v4', W[0])] - (c[(s, '元', W[0])] - 0.03) for s in S],
      'C7_v4_reunion>0': [c[(s, 'v4', W[1])] for s in S],
      'C8_v4_gaze>B0': [c[(s, 'v4', W[2])] - c[(s, '元', W[2])] for s in S],
      'C9_v4_imperative>B0': [c[(s, 'v4', W[3])] - c[(s, '元', W[3])] for s in S],
      'C10_v4_declarative_growth>0': [c[(s, 'v4', W[4])] for s in S],
    }
    res = {k: dict(pass_worlds=int(sum(v > 0 for v in x)) if k.startswith('C6') is False else int(sum(v >= 0 for v in x)), median_CI95=boot(x)) for k, x in d.items()}
    for k in res: res[k]['pass'] = res[k]['pass_worlds'] >= 20
    print(json.dumps(res, ensure_ascii=False))
    json.dump(dict(結果=res, 差=d, 行=[list(x) for x in r]), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
