import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S48R', '../S48_得と邪魔を分ける_20261118/走らせる.py')
B, W = P.B, P.W
def 一生(s, 腕, 寿命=8000, 感=64, 雑=0.6):
    W.感覚数 = 感; W.見た目雑音 = 雑
    try: return P.一生(s, 腕, 寿命)
    finally: W.感覚数 = 256; W.見た目雑音 = 0.3
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, B.区(o, 0, 500)[2], float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]])))
腕 = ['本物', 'ずらし', '道具']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        W.感覚数 = 64; c = B.換算(18399, 0, '獲得型'); print('感覚の W:', c.感覚.W.shape); W.感覚数 = 256
        a = 一生(18399, '本物', 600); b = 一生(18399, '本物', 600, 256, 0.3); d = 一生(18399, '本物', 600, 256, 0.6)
        print('64/0.6≠256/0.3:', a['sha256'] != b['sha256'], ' 雑音だけ変えても違う:', b['sha256'] != d['sha256'], ' 256/0.3＝S48:', b['sha256'] == P.一生(18399, '本物', 600)['sha256'])
        x = [一生(18399, k, 600)['sha256'] for k in 腕]; print('3腕が違う:', len(set(x)) == 3); sys.exit()
    段 = sys.argv[1]; S = range(18200, 18230) if 段 == '本' else range(18300, 18330)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): (f, g) for s, a, f, g in r}
    res = dict(H1_本物は道具より大きい=int(sum(d[(s, '本物')][1] > d[(s, '道具')][1] for s in S)), H2_ずらしは道具より小さい=int(sum(d[(s, 'ずらし')][1] < d[(s, '道具')][1] for s in S)),
               H3_育ち本物が道具より大きい=int(sum(d[(s, '本物')][1] - d[(s, '本物')][0] > d[(s, '道具')][1] - d[(s, '道具')][0] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: [round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in range(2)] for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
