import sys, numpy as np
sys.path.insert(0, '../S233_耳の型は増えるか_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何, k = job; return (数え.増える if 何 == '増' else 数え.得)(s, k)[0]
if __name__ == '__main__':
    J = [(s, 何, k) for 何, k in [('増', 50.0), ('増', 0.0), ('得', 50.0)] for s in range(900, 910)]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, J, chunksize=1)
    R = {}
    for (s, 何, k), v in zip(J, r): R.setdefault((何, k), []).append(v)
    for key, v in R.items(): v = np.array(v); print(key, np.round(v, 3).tolist(), '中央値', round(float(np.median(v)), 3), flush=True)
    a, b, g = np.array(R[('増', 50.0)]), np.array(R[('増', 0.0)]), np.array(R[('得', 50.0)])
    print(f'共感ありで耳>4 {int((a > 4).sum())}/10・共感あり>なし {int((a > b).sum())}/10・耳が得（>0） {int((g > 0).sum())}/10')
