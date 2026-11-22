import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
腕 = {'β0.3_親切': (0.3, 3.0), 'β0.3_対照': (0.3, 1.0), 'β0_親切': (0.0, 3.0)}
def one(job):
    sp = importlib.util.spec_from_file_location('S208数え', '../S208_損な親切は減るか_20261121/数え.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    s, 名 = job; β, k = 腕[名]; return (s, 名) + m.測る(s, 1.0, β=β, 親切=k)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(43400, 43430) if 段 == '本' else range(43500, 43530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_寄れば残る': int(sum(d[(s, 'β0.3_親切')][0] > 0 for s in S)), 'H2_寄るおかげ': int(sum(d[(s, 'β0.3_親切')][0] > d[(s, 'β0_親切')][0] for s in S)), 'H3_有利に広がる': int(sum(d[(s, 'β0.3_親切')][0] > d[(s, 'β0.3_対照')][0] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(終わり=round(float(np.median([d[(s, 名)][0] for s in S])), 2), 終わり0の世界=int(sum(d[(s, 名)][0] == 0 for s in S))) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
