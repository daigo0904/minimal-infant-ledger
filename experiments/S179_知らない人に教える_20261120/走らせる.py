import sys, json, numpy as np
sys.path.insert(0, '../S179_知らない人に教える_20261120')
from multiprocessing import Pool
def one(job):
    import 数え; return job + 数え.測る(*job)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(37200, 37230) if 段 == '本' else range(37300, 37330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in ['元', 'v4'] for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 60
    res = {'H1_知らない時に教える': sum(d[(s, 'v4')][0] > 0 for s in S), 'H2_育つ': sum(d[(s, 'v4')][0] > d[(s, 'v4')][1] for s in S), 'H3_v4のおかげ': sum(d[(s, 'v4')][0] > d[(s, '元')][0] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['終わり差', '初め差', '初め_知らない指す', '初め_知っている指す', '初め_知っている取る', '初め_知らない取る', '終わり_知らない指す', '終わり_知っている指す', '終わり_知っている取る', '終わり_知らない取る'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(10)])) for 名 in ['元', 'v4']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
