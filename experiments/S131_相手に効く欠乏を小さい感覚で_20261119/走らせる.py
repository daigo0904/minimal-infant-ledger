import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
T129 = L('S129走', '../S129_相手に効く欠乏_20261119/走らせる.py'); R = T129.R
def 小さく(): R.W.感覚数 = 64; R.N.見た目雑音 = 0.6
def one(job): 小さく(); return T129.one(job)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        小さく(); c = R.B.換算(29799, 0, '獲得型'); print('感覚の W:', c.感覚.W.shape, '雑音', R.N.見た目雑音)
        print({kD: [round(x, 3) for x in one((29799, kD))[2:]] for kD in [0.0, 30.0]}); sys.exit()
    段 = sys.argv[1]; S = range(29600, 29630) if 段 == '本' else range(29700, 29730)
    with Pool(8) as p: r = p.map(one, [(s, kD) for kD in [0.0, 30.0] for s in S])
    d = {(s, kD): v for s, kD, *v in r}
    増 = lambda s, kD: d[(s, kD)][0] - d[(s, kD)][1]
    res = {'H1_戻った時に増える': int(sum(増(s, 30.0) > 0 for s in S)), 'H2_元の頭より大きい': int(sum(増(s, 30.0) > 増(s, 0.0) for s in S)), 'H3_見られ分けを壊さない': int(sum(d[(s, 30.0)][2] >= d[(s, 0.0)][2] - 0.03 for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kD{kD}': dict(P養_欠乏=round(float(np.median([d[(s, kD)][0] for s in S])), 3), P養_なし=round(float(np.median([d[(s, kD)][1] for s in S])), 3), 増え=round(float(np.median([増(s, kD) for s in S])), 3), 見られ分け=round(float(np.median([d[(s, kD)][2] for s in S])), 3)) for kD in [0.0, 30.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
