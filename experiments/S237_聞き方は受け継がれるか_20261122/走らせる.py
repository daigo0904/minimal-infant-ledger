import sys, json, numpy as np
sys.path.insert(0, '../S237_聞き方は受け継がれるか_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何 = job; x = (数え.増える(s)[0], 0.0, 0.0) if 何 == '増' else tuple(数え.得(s)[:3]); return (s, 何) + x
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(49000, 49030) if 段 == '本' else range(49100, 49130))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 何) for 何 in ['増', '得'] for s in S], chunksize=1)
    d = {(s, 何): x for s, 何, *x in r}; assert len(d) == 60
    res = {'H1_分けて聞く子が増える': int(sum(d[(s, '増')][0] > 4 for s in S)), 'H2_分けて聞く子が得': int(sum(d[(s, '得')][0] > 0 for s in S)), 'H3_聞き手としてよく当たる': int(sum(d[(s, '得')][1] > d[(s, '得')][2] for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = dict(終わりの分けて聞く子=float(np.median([d[(s, '増')][0] for s in S])), 空腹差_まとめて引く分けて=round(float(np.median([d[(s, '得')][0] for s in S])), 4), 当たり_分けて=round(float(np.median([d[(s, '得')][1] for s in S])), 3), 当たり_まとめて=round(float(np.median([d[(s, '得')][2] for s in S])), 3))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
