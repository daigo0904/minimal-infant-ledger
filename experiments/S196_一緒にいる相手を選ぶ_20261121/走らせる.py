import sys, json, numpy as np
sys.path.insert(0, '../S196_一緒にいる相手を選ぶ_20261121')
from multiprocessing import Pool
腕 = {'β0_kG1': (0.0, 1.0), 'β0.3_kG0': (0.3, 0.0), 'β0.3_kG1': (0.3, 1.0)}
def one(job):
    import 数え; s, 名 = job; β, k = 腕[名]; return (s, 名) + 数え.測る(s, β, kG=k)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(40600, 40630) if 段 == '本' else range(40700, 40730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_寄ると一緒の相手が偏る': sum(d[(s, 'β0.3_kG1')][2] > d[(s, 'β0_kG1')][2] for s in S), 'H2_寄ると親友': sum(d[(s, 'β0.3_kG1')][1] > d[(s, 'β0_kG1')][1] for s in S),
           'H3_親友は感謝のおかげ': sum(d[(s, 'β0.3_kG1')][1] > d[(s, 'β0.3_kG0')][1] for s in S), 'H4_一緒も感謝のおかげ': sum(d[(s, 'β0.3_kG1')][2] > d[(s, 'β0.3_kG0')][2] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['相関', 'なぐさめ先の偏り', '会う偏り'], [round(float(np.nanmedian([d[(s, 名)][j] for s in S])), 4) for j in range(3)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
