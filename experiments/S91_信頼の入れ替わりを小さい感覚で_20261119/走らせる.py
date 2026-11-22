import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = L('S90R', '../S90_信頼の入れ替わり_20261119/走らせる.py')
B, W, N = P.B, P.W, P.N
def 一生(s, 替える, 寿命=8000, 感=64, 雑=0.6):
    W.感覚数 = 感; N.見た目雑音 = 雑
    try: return P.一生(s, 替える, 寿命)
    finally: W.感覚数 = 256; N.見た目雑音 = 0.3
def one(job):
    s, v = job; o = 一生(s, v); return (s, v) + P.数(o, 3000, 4000) + P.数(o, 7000, 8000)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        W.感覚数 = 64; W.行動数 = 16; W.見た目次元 = 25; c = B.換算(21799, 2, '獲得型'); print('感覚の W:', c.感覚.W.shape); W.感覚数 = 256; W.行動数 = 4; W.見た目次元 = 8
        a = 一生(21799, True, 600); b = 一生(21799, True, 600, 256, 0.3); d = 一生(21799, True, 600, 256, 0.6)
        print('64/0.6≠256/0.3:', a['sha256'] != b['sha256'], ' 雑音だけでも違う:', b['sha256'] != d['sha256'], ' 256/0.3＝S90:', b['sha256'] == P.一生(21799, True, 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(21600, 21630) if 段 == '本' else range(21700, 21730)
    with Pool(8) as p: r = p.map(one, [(s, v) for v in [False, True] for s in S])
    d = {(s, v): x for s, v, *x in r}
    res = dict(H1_入れ替え後は新しいお手本を多く写す=int(sum(d[(s, True)][4] > d[(s, True)][3] for s in S)), H2_入れ替えで写す相手が逆転する=int(sum((d[(s, True)][4] - d[(s, True)][3]) - (d[(s, False)][4] - d[(s, False)][3]) > 0 for s in S)),
               参考_入れ替え前は赤ちゃん0を多く写す=int(sum(d[(s, True)][0] > d[(s, True)][1] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_入れ替え後は新しいお手本を多く写す', 'H2_入れ替えで写す相手が逆転する']}
    名 = ['前_0を写す', '前_1を写す', '前_他', '後_0を写す', '後_1を写す', '後_他']
    res['中央値'] = {('替える' if v else '替えない'): {名[k]: round(float(np.median([d[(s, v)][k] for s in S])), 3) for k in range(6)} for v in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
