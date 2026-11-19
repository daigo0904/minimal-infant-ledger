import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S = L('S129選び', '../S129_相手に効く欠乏_20261119/選び.py'); G, R = S.G, S.R
G.設定.update(目安=0.05, 速=400.0)
def one(job):
    s, kD = job; G.設定.update(目安=0.05, 速=400.0); a = S.一生(s, '欠乏', kD); b = S.一生(s, 'なし', kD)
    return (s, kD, R.P養(a, 7500, 7700), R.P養(b, 7500, 7700), float(np.mean([R.B.区(b, 7000, 7500)[2], R.B.区(b, 7500, 8000)[2]])), float(b['食列'][7000:].mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 29399; 元 = L('S64元', '../S64_構われないと_20261118/走らせる.py')
        print('kD=0 は S64 と同じ sha:', S.一生(s, '欠乏', 0.0)['sha256'] == 元.一生(s, '欠乏')['sha256'], ' kD=30 で手が変わる:', S.一生(s, '欠乏', 30.0)['sha256'] != 元.一生(s, '欠乏')['sha256'])
        print({kD: [round(x, 3) for x in one((s, kD))[2:]] for kD in [0.0, 30.0]}); sys.exit()
    段 = sys.argv[1]; T = range(29200, 29230) if 段 == '本' else range(29300, 29330)
    with Pool(8) as p: r = p.map(one, [(s, kD) for kD in [0.0, 30.0] for s in T])
    d = {(s, kD): v for s, kD, *v in r}
    増 = lambda s, kD: d[(s, kD)][0] - d[(s, kD)][1]
    res = {'H1_相手に効く欠乏で戻った時に増える': int(sum(増(s, 30.0) > 0 for s in T)), 'H2_増えが元の頭より大きい': int(sum(増(s, 30.0) > 増(s, 0.0) for s in T)),
           'H3_普段の見られ分けを壊さない（元−0.03 以上）': int(sum(d[(s, 30.0)][2] >= d[(s, 0.0)][2] - 0.03 for s in T))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'kD{kD}': dict(P養_欠乏=round(float(np.median([d[(s, kD)][0] for s in T])), 3), P養_なし=round(float(np.median([d[(s, kD)][1] for s in T])), 3), 増え=round(float(np.median([増(s, kD) for s in T])), 3), 見られ分け=round(float(np.median([d[(s, kD)][2] for s in T])), 3), 食べ=round(float(np.median([d[(s, kD)][3] for s in T])), 4)) for kD in [0.0, 30.0]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
