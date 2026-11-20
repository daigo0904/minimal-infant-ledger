import sys, json, numpy as np
sys.path.insert(0, '../S197_両思いで長続き_20261121')
from multiprocessing import Pool
腕 = {'β0_kG1': (0.0, 1.0), 'β0.3_kG0': (0.3, 0.0), 'β0.3_kG1': (0.3, 1.0)}
def one(job):
    import 数え; s, 名 = job; return (s, 名) + 数え.測る(s, *腕[名])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(41000, 41030) if 段 == '本' else range(41100, 41130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_両思い': sum(d[(s, 'β0.3_kG1')][0] > 0.143 for s in S), 'H2_長続き': sum(d[(s, 'β0.3_kG1')][1] > 0.143 for s in S), 'H3_寄るおかげの両思い': sum(d[(s, 'β0.3_kG1')][0] > d[(s, 'β0_kG1')][0] for s in S),
           'H4_感謝のおかげの両思い': sum(d[(s, 'β0.3_kG1')][0] > d[(s, 'β0.3_kG0')][0] for s in S), 'H5_感謝のおかげの長続き': sum(d[(s, 'β0.3_kG1')][1] > d[(s, 'β0.3_kG0')][1] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['両思い', '長続き'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(2)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
