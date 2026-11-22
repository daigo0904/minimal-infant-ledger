import sys, json, numpy as np
sys.path.insert(0, '../S198_人気者と仲間はずれ_20261121')
from multiprocessing import Pool
腕 = {'β0_kG1': (0.0, 1.0), 'β0.3_kG0': (0.3, 0.0), 'β0.3_kG1': (0.3, 1.0)}
def one(job):
    import 数え; s, 名 = job; return (s, 名) + 数え.測る(s, *腕[名])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(41200, 41230) if 段 == '本' else range(41300, 41330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    g = lambda v, 既定: 既定 if v != v else v
    res = {'H1_外れると空腹': sum(g(d[(s, 'β0.3_kG1')][2], -9) > 0 for s in S), 'H2_なぐさめが届かない': sum(g(d[(s, 'β0.3_kG1')][3], 9) < 0 for s in S),
           'H3_寄るせいで外れが困る': sum(g(d[(s, 'β0.3_kG1')][2], -9) > g(d[(s, 'β0_kG1')][2], 9) for s in S), 'H4_寄ると外れる子が増える': sum(d[(s, 'β0.3_kG1')][0] > d[(s, 'β0_kG1')][0] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['外れの数', 'ジニ', '空腹差', 'なぐさめてもらった差'], [round(float(np.nanmedian([d[(s, 名)][j] for s in S])), 4) for j in range(4)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
