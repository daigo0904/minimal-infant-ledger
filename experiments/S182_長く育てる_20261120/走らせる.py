import sys, json, os, numpy as np
sys.path.insert(0, '../S182_長く育てる_20261120')
from multiprocessing import Pool
def one(job):
    import 数え; s, α = job; return [s, α] + list(数え.測る(s, α))
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(37800, 37830) if 段 == '本' else range(37900, 37930)); 書 = f'結果_{段}.jsonl'; 済 = {}
    if os.path.exists(書):
        for l in open(書): x = json.loads(l); 済[(x[0], x[1])] = x[2:]
    jobs = [(s, α) for α in [None, 0.5] for s in S if (s, α) not in 済]; print('残り', len(jobs), '本', file=sys.stderr, flush=True)
    with Pool(8, maxtasksperchild=1) as p, open(書, 'a') as f:
        for x in p.imap_unordered(one, jobs, chunksize=1): f.write(json.dumps(x, ensure_ascii=False) + '\n'); f.flush(); 済[(x[0], x[1])] = x[2:]
    assert len(済) == 60, len(済)
    d = 済
    res = {'H1_長く育てば教える': sum(d[(s, 0.5)][3] > 0 for s in S), 'H2_教えが育つ': sum(d[(s, 0.5)][3] > d[(s, 0.5)][0] for s in S), 'H3_損を取り戻す': sum(d[(s, 0.5)][5] > d[(s, None)][5] for s in S), 'H4_記憶のおかげ': sum(d[(s, 0.5)][3] > d[(s, None)][3] for s in S)}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'記憶{α}': dict(zip(['6000-8000指す差', '6000-8000取る差', '6000-8000食べ', '終わり指す差', '終わり取る差', '終わり食べ'], [round(float(np.median([d[(s, α)][j] for s in S])), 4) for j in range(6)])) for α in [None, 0.5]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
