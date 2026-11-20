import sys, json, numpy as np
sys.path.insert(0, '../S180_記憶が要る知らない_20261120')
from multiprocessing import Pool
腕 = {'見える': ('v4', False, 'いない時'), '隠す': ('v4', True, 'いない時')}
def one(job):
    import 数え; s, 名 = job; return (s, 名) + 数え.測る(s, *腕[名])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(37400, 37430) if 段 == '本' else range(37500, 37530))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 60
    res = {'H1_見えなくても見分ける': sum(d[(s, '隠す')][0] > 0 for s in S), 'H2_見えるほうが見分ける': sum(d[(s, '見える')][0] > d[(s, '隠す')][0] for s in S), 'H3_知らないことが損': sum(d[(s, '見える')][10] > d[(s, '隠す')][10] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['終わり差', '初め差', '初め_知らない指す', '初め_知っている指す', '初め_知っている取る', '初め_知らない取る', '終わり_知らない指す', '終わり_知っている指す', '終わり_知っている取る', '終わり_知らない取る', '食べ'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(11)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
