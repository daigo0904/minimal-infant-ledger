import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S59R', '../S59_養育者と親友_20261118/走らせる.py')
B, W, N = P.B, P.W, P.N
子 = []
def 一生(s, 腕, 寿命=8000, 感=64, 雑=0.6):
    W.感覚数 = 感; N.見た目雑音 = 雑
    try:
        o = P.一生(s, 腕, 寿命); return o
    finally: W.感覚数 = 256; N.見た目雑音 = 0.3
def one(job):
    s, 腕 = job; o = 一生(s, 腕); return (s, 腕, P.割(o, 7000, 8000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        W.感覚数 = 64; W.見た目次元 = 12; c = B.換算(16199, 0, '獲得型'); print('感覚の W:', c.感覚.W.shape, ' Q:', c.Q.shape); W.感覚数 = 256; W.見た目次元 = 8
        a = 一生(16199, '本物', 300); b = 一生(16199, '本物', 300, 256, 0.3)
        print('64/0.6 ≠ 256/0.3:', a['sha256'] != b['sha256'], ' 256/0.3 ＝ S59:', b['sha256'] == P.一生(16199, '本物', 300)['sha256'])
        N.見た目雑音 = 0.6; 世 = np.random.default_rng([16199, 0]); print('世界の雑音設定:', N.見た目雑音); N.見た目雑音 = 0.3; sys.exit()
    段 = sys.argv[1]; S = range(16000, 16030) if 段 == '本' else range(16100, 16130)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['本物', '道具'] for s in S])
    d = {(s, a): x for s, a, x in r}
    差 = lambda s, a: d[(s, a)]['友手_友'] - d[(s, a)]['友手_他']
    res = dict(H1_親友の前で親友の手=int(sum(差(s, '本物') > 0 for s in S)), H2_養育者の前で一番の手=int(sum(d[(s, '本物')]['一番_養'] > d[(s, '本物')]['一番_友'] for s in S)), H3_親友の分け_本物が道具より=int(sum(差(s, '本物') > 差(s, '道具') for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: {k: round(float(np.median([d[(s, a)][k] for s in S])), 3) for k in ['友手_友', '友手_他', '一番_養', '一番_友']} for a in ['本物', '道具']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
