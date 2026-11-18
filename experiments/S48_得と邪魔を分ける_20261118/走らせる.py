import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
sp = importlib.util.spec_from_file_location('S47', '../S47_本物とずらし_20261118/走らせる.py'); S47 = importlib.util.module_from_spec(sp); sp.loader.exec_module(S47)
B = S47.B; W = S47.W
def 一生(s, 腕, 寿命=8000):
    if 腕 != '道具': return S47.一生(s, 腕, 寿命)
    W.学び率 = 0.01; W.赤ちゃん = B.原
    try: return W.一生(s, '依存', '道具型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, B.区(o, 0, 500)[2], float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]])))
腕 = ['本物', 'ずらし', '道具']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(13099, a, 600)['sha256'] for a in 腕]; print('3腕が互いに違う:', len(set(x)) == 3); sys.exit()
    段 = sys.argv[1]; S = range(13000, 13030) if 段 == '本' else range(13100, 13130)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): (f, g) for s, a, f, g in r}
    res = dict(H1_本物は道具より大きい=int(sum(d[(s, '本物')][1] > d[(s, '道具')][1] for s in S)), H2_ずらしは道具より小さい=int(sum(d[(s, 'ずらし')][1] < d[(s, '道具')][1] for s in S)),
               H3_育ち本物が道具より大きい=int(sum(d[(s, '本物')][1] - d[(s, '本物')][0] > d[(s, '道具')][1] - d[(s, '道具')][0] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: [round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in range(2)] for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
