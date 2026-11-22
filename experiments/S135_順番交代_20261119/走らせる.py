import sys, json, numpy as np
sys.path.insert(0, '../S135_順番交代_20261119')
from multiprocessing import Pool
from 共 import *
def one(job): s, 番 = job; o = 一生(s, 番); return (s, 番) + 数える(o, 0, 1000) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    段 = sys.argv[1]; S = range(30000, 30030) if 段 == '本' else range(30100, 30130)
    with Pool(8) as p: r = p.map(one, [(s, 番) for 番 in ['交代', 'でたらめ'] for s in S])
    d = {(s, 番): v for s, 番, *v in r}
    res = {'H1_順番交代が育つ（差 終わり>初め）': int(sum(d[(s, '交代')][6] > d[(s, '交代')][2] for s in S)), 'H2_交代の世界でだけ（交代>でたらめ）': int(sum(d[(s, '交代')][6] > d[(s, 'でたらめ')][6] for s in S)),
           'H3_相手が話す時に待つようになる（話す時の声 終わり<初め）': int(sum(d[(s, '交代')][5] < d[(s, '交代')][1] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_聞く時に声', '初め_話す時に声', '初め_差', '初め_食べ', '終わり_聞く時に声', '終わり_話す時に声', '終わり_差', '終わり_食べ']
    res['中央値'] = {番: {n: round(float(np.median([d[(s, 番)][j] for s in S])), 4) for j, n in enumerate(名)} for 番 in ['交代', 'でたらめ']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
