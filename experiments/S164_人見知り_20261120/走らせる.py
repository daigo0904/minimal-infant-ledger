import sys, json, numpy as np
sys.path.insert(0, '../S164_人見知り_20261120')
from multiprocessing import Pool
from 共 import *
def one(job):
    s, 名 = job; o = 一生(s, '見る', 名, 知らない=(4000, 0.3)); r = []
    for lo, hi in [(4000, 5000), (7000, 8000)]:
        x = 人見(o, lo, hi); r += [(x[0] + x[2]) / 2 - (x[4] + x[6]) / 2, (x[1] + x[3]) / 2 - (x[5] + x[7]) / 2, (x[0] + x[2]) / 2, (x[1] + x[3]) / 2]
    return (s, 名) + tuple(r)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(34800, 34830) if 段 == '本' else range(34900, 34930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in ['元', 'v4'] for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 60
    res = {'H1_控える': sum(d[(s, 'v4')][0] < 0 for s in S), 'H2_顔を見る': sum(d[(s, 'v4')][1] > 0 for s in S), 'H3_大胆': sum(d[(s, 'v4')][0] > 0 for s in S),
           '参考_元_控える': sum(d[(s, '元')][0] < 0 for s in S), '参考_元_顔を見る': sum(d[(s, '元')][1] > 0 for s in S),
           '参考_v4_慣れた後_控える': sum(d[(s, 'v4')][4] < 0 for s in S), '参考_v4_慣れた後_大胆': sum(d[(s, 'v4')][4] > 0 for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_控える', 'H2_顔を見る', 'H3_大胆']}
    res['中央値'] = {名: dict(zip(['会い始め_取る差', '会い始め_見る差', '会い始め_知らないで取る', '会い始め_知らないで見る', '慣れた後_取る差', '慣れた後_見る差', '慣れた後_取る', '慣れた後_見る'], [round(float(np.median([d[(s, 名)][j] for s in S])), 3) for j in range(8)])) for 名 in ['元', 'v4']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
