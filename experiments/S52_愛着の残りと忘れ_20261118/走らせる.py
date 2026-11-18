import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S50R', '../S50_相手の直前の手が見える_20261118/走らせる.py')   # S50 の世界（12次元入力・仲間へ）と本物の頭
B, W, N = R.B, R.W, R.N
子 = []
class 見る(B.換算):
    def __init__(s, *a): super().__init__(*a); 子.append(s)
def 一生(s, 忘れ, 寿命=16000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; W.つながり忘却 = 忘れ; N.赤ちゃん = 見る; 子.clear()
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='仲間へ', 切替=8000)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8; W.つながり忘却 = 0.9999
def one(job):
    s, f = job; o = 一生(s, f)
    return (s, f, R.数字(o, 7000, 8000), R.数字(o, 15000, 16000), float(o['食列'][15000:16000].mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(13899, 0.999, 600); g = [c.つながり.忘れ for c in 子]; b = 一生(13899, 0.9999, 600)
        print('0.999 の子のつながりの忘れ:', set(g), ' 0.999≠0.9999:', a['sha256'] != b['sha256'], ' 0.9999＝S50 替える:', b['sha256'] == R.一生(13899, '替える', 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(13800, 13830) if 段 == '本' else range(13900, 13930)
    with Pool(8) as p: r = p.map(one, [(s, f) for f in [0.9999, 0.999] for s in S])
    d = {(s, f): (x, y, e) for s, f, x, y, e in r}
    res = dict(H1_喜ばせの残りが減る=int(sum(d[(s, 0.999)][1][0] < d[(s, 0.9999)][1][0] for s in S)), H2_合わせは損なわない=int(sum(d[(s, 0.999)][1][1] >= d[(s, 0.9999)][1][1] for s in S)),
               H3_育ちの段階は保つ=int(sum(d[(s, 0.999)][0][2] >= 0.8 * d[(s, 0.9999)][0][2] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {str(f): dict(前=[round(float(np.median([d[(s, f)][0][k] for s in S])), 3) for k in range(3)], 後=[round(float(np.median([d[(s, f)][1][k] for s in S])), 3) for k in range(3)], 食べた=round(float(np.median([d[(s, f)][2] for s in S])), 4)) for f in [0.9999, 0.999]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
