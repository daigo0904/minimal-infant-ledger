import sys, json, numpy as np
sys.path.insert(0, '../S199_困っている子にも寄る_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(41400, 41430) if 段 == '本' else range(41500, 41530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, γ) for γ in [0.0, 5.0] for s in S], chunksize=1)
    d = {(s, γ): v for s, γ, *v in r}; assert len(d) == 60
    z = lambda v: 0.0 if v != v else v
    res = {'H1_外れの害が減る': sum(z(d[(s, 5.0)][0]) < z(d[(s, 0.0)][0]) for s in S), 'H2_外れにも助けが届く': sum(z(d[(s, 5.0)][1]) > z(d[(s, 0.0)][1]) for s in S), 'H3_みんなが楽': sum(d[(s, 5.0)][4] < d[(s, 0.0)][4] for s in S),
           'H4_会う偏りが弱まる': sum(d[(s, 5.0)][2] < d[(s, 0.0)][2] for s in S), 'H5_両思いが弱まる': sum(d[(s, 5.0)][3] < d[(s, 0.0)][3] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'γ{γ}': dict(zip(['外れの空腹差', 'なぐさめてもらった差', '会う偏り', '両思い', '全体の空腹', '外れの数'], [round(float(np.nanmedian([d[(s, γ)][j] for s in S])), 4) for j in range(6)])) for γ in [0.0, 5.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
