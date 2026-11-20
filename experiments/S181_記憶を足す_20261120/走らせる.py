import sys, json, numpy as np
sys.path.insert(0, '../S181_記憶を足す_20261120')
from multiprocessing import Pool
def one(job):
    import 数え; s, α = job; return (s, α) + 数え.測る(s, 'v4', True, 'いない時', 記憶=α)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(37600, 37630) if 段 == '本' else range(37700, 37730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, α) for α in [None, 0.5] for s in S], chunksize=1)
    d = {(s, α): v for s, α, *v in r}; assert len(d) == 60
    取差 = lambda s, α: d[(s, α)][8] - d[(s, α)][9]
    res = {'H1_知らない時に教える': sum(d[(s, 0.5)][0] > 0 for s in S), 'H2_知っている時に取る': sum(取差(s, 0.5) > 0 for s in S), 'H3_記憶のおかげ': sum(取差(s, 0.5) > 取差(s, None) for s in S), 'H4_損を取り戻す': sum(d[(s, 0.5)][10] > d[(s, None)][10] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'記憶{α}': dict(zip(['終わり指す差', '初め指す差', '初め_知らない指す', '初め_知っている指す', '初め_知っている取る', '初め_知らない取る', '終わり_知らない指す', '終わり_知っている指す', '終わり_知っている取る', '終わり_知らない取る', '食べ'], [round(float(np.median([d[(s, α)][j] for s in S])), 4) for j in range(11)]), 取差=round(float(np.median([取差(s, α) for s in S])), 4)) for α in [None, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
