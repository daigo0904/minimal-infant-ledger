import sys, json, numpy as np
sys.path.insert(0, '../S235_組み合わせる言葉_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(48600, 48630) if 段 == '本' else range(48700, 48730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in ['耳', 'ふつう'] for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 60; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_耳で組み立てる': int(sum(v(s, '耳', 0) > v(s, 'ふつう', 0) for s in S)), 'H2_未見も伝わる': int(sum(v(s, '耳', 3) > 3 / 16 for s in S)), 'H3_未見がふつうより伝わる': int(sum(v(s, '耳', 3) > v(s, 'ふつう', 3) for s in S)), 'H4_未見は偶然より低い': int(sum(v(s, '耳', 3) < 1 / 16 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    名 = ['組み立て度', '全体の情報', '当たり', '未見の当たり_最初1000', '未見の当たり_4000']
    res['中央値'] = {k: {n: round(float(np.median([v(s, k, j) for s in S])), 3) for j, n in enumerate(名)} for k in ['耳', 'ふつう']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
