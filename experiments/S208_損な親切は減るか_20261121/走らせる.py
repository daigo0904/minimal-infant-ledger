import sys, json, numpy as np
sys.path.insert(0, '../S208_損な親切は減るか_20261121')
from multiprocessing import Pool
腕 = {'kG0': (0.0, 3.0), 'kG1': (1.0, 3.0), '対照': (1.0, 1.0)}
def one(job):
    import 数え; s, 名 = job; g, k = 腕[名]; return (s, 名) + 数え.測る(s, g, 親切=k)
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(43200, 43230) if 段 == '本' else range(43300, 43330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_感謝なしで減る': int(sum(d[(s, 'kG0')][0] < 4 for s in S)), 'H2_感謝ありでも減る': int(sum(d[(s, 'kG1')][0] < 4 for s in S)),
           'H3_損のせい_対照': int(sum(d[(s, '対照')][0] > d[(s, 'kG1')][0] for s in S)), 'H4_感謝で遅い': int(sum(d[(s, 'kG1')][1] > d[(s, 'kG0')][1] for s in S))}
    res['判定'] = {'H1_感謝なしで減る': res['H1_感謝なしで減る'] >= 20, 'H2_感謝ありでも減る': res['H2_感謝ありでも減る'] >= 20, 'H3_損のせい_対照': res['H3_損のせい_対照'] >= 10, 'H4_感謝で遅い': res['H4_感謝で遅い'] >= 20}
    res['中央値'] = {名: dict(終わり=round(float(np.median([d[(s, 名)][0] for s in S])), 2), 中ほど=round(float(np.median([d[(s, 名)][1] for s in S])), 2), 終わり0の世界=int(sum(d[(s, 名)][0] == 0 for s in S))) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
