import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
D = L('S128診断', '../S128_癖を弱めても甘えない理由_20261119/診断.py')
def one(job): s, e, λ = job; return (s, e, λ) + tuple(float(x) for x in D.one((s, e, λ)))
名 = ['Q差', 'つながり差', '合計', 'P養', '欠乏前つながり差', '勝つ割合', '勝ち負けの差_中央値', '負けている時の差']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 29199; 元 = L('S64元', '../S64_構われないと_20261118/走らせる.py')
        print('λ=1 の記録つきは S64 と同じ sha:', D.一生(s, True, 1.0)['sha256'] == 元.一生(s, '欠乏')['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(29000, 29030) if 段 == '本' else range(29100, 29130)
    with Pool(8) as p: r = p.map(one, [(s, e, λ) for λ in [1.0, 0.2] for e in [False, True] for s in S])
    d = {(s, e, λ): v for s, e, λ, *v in r}
    res = {}
    for λ in [1.0, 0.2]:
        res[f'λ{λ}_H1_勝つ時の差が広がる'] = int(sum(d[(s, True, λ)][6] > d[(s, False, λ)][6] for s in S))
        res[f'λ{λ}_H2_負ける時の差が深まる'] = int(sum(d[(s, True, λ)][7] < d[(s, False, λ)][7] for s in S))
        res[f'λ{λ}_H3_勝つ割合は増えない'] = int(sum(d[(s, True, λ)][5] <= d[(s, False, λ)][5] for s in S))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'λ{λ}_{"欠乏" if e else "なし"}': {n: round(float(np.median([d[(s, e, λ)][j] for s in S])), 4) for j, n in enumerate(名)} for λ in [1.0, 0.2] for e in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
