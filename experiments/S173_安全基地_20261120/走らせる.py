import sys, json, numpy as np
sys.path.insert(0, '../S173_安全基地_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): return job + 測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(36000, 36030) if 段 == '本' else range(36100, 36130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in ['元', 'v4'] for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 60
    def 数(名): return {'H1_安全基地': sum(d[(s, 名)][0] > 0 for s in S), 'H2_確かめてから': sum(d[(s, 名)][1] > 0 for s in S), 'H3_逆の向き': sum(d[(s, 名)][0] < 0 for s in S), 'H4_分からない物だけの差': sum(d[(s, 名)][0] < d[(s, 名)][2] for s in S)}
    res = 数('v4'); res['判定'] = {k: x >= 20 for k, x in res.items()}; res['参考_元'] = 数('元')
    res['中央値'] = {名: dict(zip(['取る差なし', '見る差なし', '取る差あり', '見る差あり', 'なし養育者取る', 'なし養育者見る', 'なし仲間取る', 'なし仲間見る'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(8)])) for 名 in ['元', 'v4']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
