import sys, json, numpy as np
sys.path.insert(0, '../S185_見られ分けの余韻_20261121')
from multiprocessing import Pool
from 共 import *
腕 = {'元_なし': ('元', None), '元_記憶': ('元', 0.5), 'v4_なし': ('v4', None), 'v4_記憶': ('v4', 0.5)}
def one(job): s, 名 = job; h, α = 腕[名]; o = 一生(s, h, 記憶=α); return (s, 名) + 余韻(o, 7000, 8000) + (float(o['食列'][7000:].mean()), o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(38400, 38430) if 段 == '本' else range(38500, 38530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 120
    res = {'H1_元に余韻': sum(d[(s, '元_記憶')][0] > 0 for s in S), 'H2_余韻は記憶のおかげ': sum(d[(s, '元_記憶')][0] > d[(s, '元_なし')][0] for s in S),
           'H3_v4に余韻': sum(d[(s, 'v4_記憶')][0] > 0 for s in S), 'H4_記憶はv4の見られ分けを弱める': sum(d[(s, 'v4_記憶')][3] < d[(s, 'v4_なし')][3] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['余韻', '直後', '続き', '見られ分け', '食べ'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(5)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
