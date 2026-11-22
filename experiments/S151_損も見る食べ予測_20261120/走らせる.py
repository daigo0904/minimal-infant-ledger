import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S151選び', '../S151_損も見る食べ予測_20261120/選び.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def one(job): s, 名 = job; return (s, 名) + tuple(G.one(job))
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(32600, 32630) if 段 == '本' else range(32700, 32730)
    with Pool(8) as p: r = p.map(one, [(s, 名) for 名 in ['v3', 'v3損も'] for s in S])
    d = {(s, 名): v for s, 名, *v in r}
    res = {'H1_損も見ると分からない時に顔を見に行く（終わりの差>0）': int(sum(d[(s, 'v3損も')][5] > 0 for s in S)),
           'H2_損もなしより見に行く': int(sum(d[(s, 'v3損も')][5] > d[(s, 'v3')][5] for s in S)),
           'H3_見に行くことが育つ（終わり>初め）': int(sum(d[(s, 'v3損も')][5] > d[(s, 'v3損も')][0] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_差', '初め_見る無', '初め_見る有', '初め_従う', '初め_食べ', '終わり_差', '終わり_見る無', '終わり_見る有', '終わり_従う', '終わり_食べ']
    res['中央値'] = {x: {n: round(float(np.median([d[(s, x)][j] for s in S])), 3) for j, n in enumerate(名)} for x in ['v3', 'v3損も']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
