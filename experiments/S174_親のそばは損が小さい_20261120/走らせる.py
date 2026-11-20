import sys, json, numpy as np
sys.path.insert(0, '../S174_親のそばは損が小さい_20261120')
from multiprocessing import Pool
from 数え import 測る
腕 = {'守りなし': (None, True), '守り0.2': (0.2, True), '守りなし_見たらF': (None, False)}
def one(job): s, 名 = job; return (s, 名) + 測る(s, 'v4', *腕[名])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(36200, 36230) if 段 == '本' else range(36300, 36330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_安全基地': sum(d[(s, '守り0.2')][0] > 0 for s in S), 'H2_守りのおかげ': sum(d[(s, '守り0.2')][0] > d[(s, '守りなし')][0] for s in S),
           'H3_任せる': sum(d[(s, '守り0.2')][1] < d[(s, '守りなし')][1] for s in S), 'H4_S173の確かめ': sum(d[(s, '守りなし_見たらF')][0] < 0 for s in S),
           'sha違う': sum(d[(s, '守り0.2')][13] != d[(s, '守りなし')][13] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_安全基地', 'H2_守りのおかげ', 'H3_任せる', 'H4_S173の確かめ']}
    res['中央値'] = {名: dict(zip(['取る差なし', '見る差なし', '取る差あり', '見る差あり', 'なし養育者取る', 'なし養育者見る', 'なし仲間取る', 'なし仲間見る'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(8)]), 食べ=round(float(np.median([d[(s, 名)][12] for s in S])), 4)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
