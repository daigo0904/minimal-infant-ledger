import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
Q = L('S51R', '../S51_入れ替わりの対照_20261118/走らせる.py')
R, B, W, N = Q.R, Q.B, Q.W, Q.N
def 一生(s, 腕, 寿命=16000, 感=64, 雑=0.6):
    W.感覚数 = 感; N.見た目雑音 = 雑
    try: return Q.一生(s, 腕, 寿命)
    finally: W.感覚数 = 256; N.見た目雑音 = 0.3
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, R.数字(o, 7000, 8000), R.数字(o, 15000, 16000), float(o['食列'][15000:16000].mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        W.感覚数 = 64; W.見た目次元 = 12; c = B.換算(18599, 0, '獲得型'); print('感覚の W:', c.感覚.W.shape); W.感覚数 = 256; W.見た目次元 = 8
        a = 一生(18599, '本物', 600); b = 一生(18599, '本物', 600, 256, 0.3); d = 一生(18599, '本物', 600, 256, 0.6)
        print('64/0.6≠256/0.3:', a['sha256'] != b['sha256'], ' 雑音だけ変えても違う:', b['sha256'] != d['sha256'], ' 256/0.3＝S51 の本物:', b['sha256'] == Q.一生(18599, '本物', 600)['sha256'], ' 本物≠道具:', a['sha256'] != 一生(18599, '道具', 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(18400, 18430) if 段 == '本' else range(18500, 18530)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['本物', '道具'] for s in S])
    d = {(s, a): (x, y, f) for s, a, x, y, f in r}
    res = dict(H1_合わせ本物が道具より大=int(sum(d[(s, '本物')][1][1] > d[(s, '道具')][1][1] for s in S)), H2_食べ物本物が道具より多=int(sum(d[(s, '本物')][2] > d[(s, '道具')][2] for s in S)),
               H3_本物の合わせが入れ替わりで増える=int(sum(d[(s, '本物')][1][1] > d[(s, '本物')][0][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(前=[round(float(np.median([d[(s, a)][0][k] for s in S])), 3) for k in range(3)], 後=[round(float(np.median([d[(s, a)][1][k] for s in S])), 3) for k in range(3)], 食べた=round(float(np.median([d[(s, a)][2] for s in S])), 4)) for a in ['本物', '道具']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
