import sys, json, numpy as np
sys.path.insert(0, '../S243_共感の見込み_20261122')
from multiprocessing import Pool
腕 = {'協力kC0': (0.0, False), '協力kC10': (10.0, False), '競うkC0': (0.0, True), '競うkC3': (3.0, True), '競うkC10': (10.0, True)}
def one(job):
    import 数え; s, 名 = job; k, c = 腕[名]; return (s, 名) + tuple(数え.測る(s, k, c))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(50200, 50230) if 段 == '本' else range(50300, 50330))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): x for s, 名, *x in r}; assert len(d) == 150; v = lambda s, 名, j: d[(s, 名)][j]
    res = {'H1_協力で共感の見込みが効く': int(sum(v(s, '協力kC10', 0) > v(s, '協力kC0', 0) for s in S)), 'H2_競うでも効く': int(sum(v(s, '競うkC10', 0) > v(s, '競うkC0', 0) for s in S)), 'H3_競うでも言葉が戻る（>0.30）': int(sum(v(s, '競うkC10', 0) > 0.30 for s in S)), 'H4_弱い見込みでは競うに負ける（kC3で>0.30）': int(sum(v(s, '競うkC3', 0) > 0.30 for s in S))}
    res['判定'] = {k: x >= 20 for k, x in res.items()}
    res['中央値'] = {名: dict(当たり=round(float(np.median([v(s, 名, 0) for s in S])), 3), 全体=round(float(np.median([v(s, 名, 1) for s in S])), 3), 話し手ごと=round(float(np.median([v(s, 名, 2) for s in S])), 3)) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
