import sys, numpy as np
sys.path.insert(0, '../S234_評判で組む_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何, ρ = job; return (数え.増える(s, ρ)[0], 0.0) if 何 == '増' else tuple(数え.得(s, ρ)[:2])
if __name__ == '__main__':
    J = [(s, 何, ρ) for 何 in ['増', '得'] for ρ in [0.0, 5.0, 10.0] for s in range(900, 910)]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, J, chunksize=1)
    R = {}
    for (s, 何, ρ), v in zip(J, r): R.setdefault((何, ρ), []).append(v)
    for k, v in R.items(): v = np.array(v); print(k, np.round(v[:, 0], 3).tolist(), '中央値', round(float(np.median(v[:, 0])), 4), ('耳どうし ' + str(round(float(np.median(v[:, 1])), 3))) if k[0] == '得' else '', flush=True)
    for ρ in [5.0, 10.0]:
        a, z, g = np.array(R[('増', ρ)])[:, 0], np.array(R[('増', 0.0)])[:, 0], np.array(R[('得', ρ)])[:, 0]
        print(f'ρ{ρ}：耳>4 {int((a > 4).sum())}/10・ρ0より多い {int((a > z).sum())}/10・耳が得 {int((g > 0).sum())}/10')
