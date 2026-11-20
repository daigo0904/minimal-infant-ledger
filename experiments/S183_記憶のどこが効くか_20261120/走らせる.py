import sys, json, os, numpy as np
sys.path.insert(0, '../S183_記憶のどこが効くか_20261120')
from multiprocessing import Pool
腕 = ['両方', '顔だけ', '手だけ']
def one(job):
    import 数え; s, 名 = job; return [s, 名] + list(数え.長く(s, 0.5, 名))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(38000, 38030) if 段 == '本' else range(38100, 38130)); 書 = f'結果_{段}.jsonl'; 済 = {}
    if os.path.exists(書):
        for l in open(書): x = json.loads(l); 済[(x[0], x[1])] = x[2:]
    jobs = [(s, 名) for 名 in 腕 for s in S if (s, 名) not in 済]; print('残り', len(jobs), '本', file=sys.stderr, flush=True)
    with Pool(8, maxtasksperchild=1) as p, open(書, 'a') as f:
        for x in p.imap_unordered(one, jobs, chunksize=1): f.write(json.dumps(x, ensure_ascii=False) + '\n'); f.flush(); 済[(x[0], x[1])] = x[2:]
    assert len(済) == 90, len(済)
    d = 済
    res = {'H1_手の記憶で教える': sum(d[(s, '手だけ')][0] > 0 for s in S), 'H2_顔の記憶で教える': sum(d[(s, '顔だけ')][0] > 0 for s in S),
           'H3_手の記憶のほうが効く': sum(d[(s, '手だけ')][0] > d[(s, '顔だけ')][0] for s in S), 'H4_両方がいちばん': sum(d[(s, '両方')][0] > d[(s, '手だけ')][0] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(zip(['指す差', '取る差', '食べ'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(3)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
