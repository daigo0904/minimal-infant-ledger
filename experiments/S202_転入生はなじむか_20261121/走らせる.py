import sys, json, numpy as np
sys.path.insert(0, '../S202_転入生はなじむか_20261121')
from multiprocessing import Pool
def one(s):
    import 数え; return (s,) + 数え.測る(s)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(42000, 42030) if 段 == '本' else range(42100, 42130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, S, chunksize=1)
    d = {x[0]: x[1:] for x in r}; assert len(d) == 30
    res = {'H1_輪になじむ': sum(d[s][5] > d[s][3] for s in S), 'H2_なぐさめも届く': sum(d[s][2] > d[s][0] for s in S), 'H3_なじみきらない': sum(d[s][2] < 0 for s in S)}
    res = {k: int(v) for k, v in res.items()}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = dict(zip(['受0', '受1', '受2', '入0', '入1', '入2'], [round(float(np.median([d[s][j] for s in S])), 3) for j in range(6)]))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
