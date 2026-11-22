import sys, json, numpy as np
sys.path.insert(0, '../S246_語ごとの手応え_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return (s, k) + tuple(数え.測る(s, '分けて', 学び方=k))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(50800, 50830) if 段 == '本' else range(50900, 50930))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, k) for k in ['分けて', '両方'] for s in S], chunksize=1)
    d = {(s, k): x for s, k, *x in r}; assert len(d) == 60; v = lambda s, k, j: d[(s, k)][j]
    res = {'H1_語ごとに学ぶと未見が伝わる': int(sum(v(s, '分けて', 3) > v(s, '両方', 3) for s in S)), 'H2_未見が半分以上伝わる': int(sum(v(s, '分けて', 3) > 0.5 for s in S)), 'H3_見た場所もよく当たる': int(sum(v(s, '分けて', 2) > v(s, '両方', 2) for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    名 = ['組み立て度', '全体の情報', '当たり', '未見の当たり_最初1000', '未見の当たり_4000']
    res['中央値'] = {f'学び方{k}': {n: round(float(np.median([v(s, k, j) for s in S])), 3) for j, n in enumerate(名)} for k in ['分けて', '両方']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
