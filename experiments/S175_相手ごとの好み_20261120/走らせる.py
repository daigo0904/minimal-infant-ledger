import sys, json, numpy as np
sys.path.insert(0, '../S175_相手ごとの好み_20261120')
from multiprocessing import Pool
from 共 import *
腕 = {'元': ('元', False), 'v4': ('v4', False), 'v4_B同じ': ('v4', True)}
def one(job):
    s, 名 = job; h, 同 = 腕[名]; o = 一生(s, h, 二人=0.5, B同じ=同); return (s, 名, 分け(o, 0, 1000), 分け(o, 7000, 8000), float(o['食列'][7000:].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(36400, 36430) if 段 == '本' else range(36500, 36530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_人ごとに分ける': sum(d[(s, 'v4')][1] > 0 for s in S), 'H2_育つ': sum(d[(s, 'v4')][1] > d[(s, 'v4')][0] for s in S),
           'H3_好みが違う時だけ': sum(d[(s, 'v4')][1] > d[(s, 'v4_B同じ')][1] for s in S), 'H4_v4のおかげ': sum(d[(s, 'v4')][1] > d[(s, '元')][1] for s in S)}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {名: dict(zip(['初め', '終わり', '食べ'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(3)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
