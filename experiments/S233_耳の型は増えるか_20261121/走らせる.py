import sys, json, numpy as np
sys.path.insert(0, '../S233_耳の型は増えるか_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何, k = job; return (s, 何, k) + tuple((数え.増える if 何 == '増' else 数え.得)(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(48200, 48230) if 段 == '本' else range(48300, 48330))
    J = [(s, 何, k) for 何, k in [('増', 50.0), ('増', 0.0), ('得', 50.0)] for s in S]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, J, chunksize=1)
    d = {(s, 何, k): x[0] for s, 何, k, *x in r}; assert len(d) == 90
    res = {'H1_共感ありで耳の子が増える': int(sum(d[(s, '増', 50.0)] > 4 for s in S)), 'H2_共感なしより多い': int(sum(d[(s, '増', 50.0)] > d[(s, '増', 0.0)] for s in S)), 'H3_耳の子は得': int(sum(d[(s, '得', 50.0)] > 0 for s in S)), 'H4_耳の子は損': int(sum(d[(s, '得', 50.0)] < 0 for s in S)), 'H5_耳の子は消える': int(sum(d[(s, '増', 50.0)] == 0 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = dict(終わりの耳の子_共感あり=float(np.median([d[(s, '増', 50.0)] for s in S])), 終わりの耳の子_共感なし=float(np.median([d[(s, '増', 0.0)] for s in S])), 空腹差_ふつう引く耳=round(float(np.median([d[(s, '得', 50.0)] for s in S])), 4))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
