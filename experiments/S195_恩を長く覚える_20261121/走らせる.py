import sys, json, numpy as np
sys.path.insert(0, '../S195_恩を長く覚える_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(40400, 40430) if 段 == '本' else range(40500, 40530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, x) for x in [0.98, 0.998] for s in S], chunksize=1)
    d = {(s, x): v for s, x, *v in r}; assert len(d) == 60
    res = {'H1_長く覚えると親友': sum(d[(s, 0.998)][1] > d[(s, 0.98)][1] for s in S), 'H2_長く覚えると組がそろう': sum(d[(s, 0.998)][0] > d[(s, 0.98)][0] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'恩薄れ{x}': dict(zip(['相関', '偏り'], [round(float(np.median([d[(s, x)][j] for s in S])), 4) for j in range(2)])) for x in [0.98, 0.998]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
