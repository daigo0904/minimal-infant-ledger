import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S50R', '../S50_相手の直前の手が見える_20261118/走らせる.py')   # S50 の世界（12次元入力・仲間へ）
Z = L('S47R', '../S47_本物とずらし_20261118/走らせる.py')         # ずらし型
B, W, N = R.B, R.W, R.N
assert Z.B is B
def 一生(s, 腕, 寿命=16000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; Z.ずらし幅[0] = 1; Z.直前の食.clear()
    N.赤ちゃん = {'本物': B.換算, 'ずらし': Z.ずらし, '道具': B.原}[腕]
    try: return N.一生(s, '依存', '道具型' if 腕 == '道具' else '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='仲間へ', 切替=8000)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, R.数字(o, 7000, 8000), R.数字(o, 15000, 16000), float(o['食列'][15000:16000].mean()))
腕 = ['本物', 'ずらし', '道具']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        x = [一生(13699, a, 600)['sha256'] for a in 腕]; print('3腕が互いに違う:', len(set(x)) == 3)
        print('本物＝S50 の替える（600手）:', 一生(13699, '本物', 600)['sha256'] == R.一生(13699, '替える', 600)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(13600, 13630) if 段 == '本' else range(13700, 13730)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): (x, y, f) for s, a, x, y, f in r}
    res = dict(H1_合わせ本物が道具より大=int(sum(d[(s, '本物')][1][1] > d[(s, '道具')][1][1] for s in S)), H2_合わせ本物がずらしより大=int(sum(d[(s, '本物')][1][1] > d[(s, 'ずらし')][1][1] for s in S)),
               H3_食べ物本物が道具より多=int(sum(d[(s, '本物')][2] > d[(s, '道具')][2] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(育前=[round(float(np.median([d[(s, a)][0][k] for s in S])), 3) for k in range(3)], 後=[round(float(np.median([d[(s, a)][1][k] for s in S])), 3) for k in range(3)], 食べた=round(float(np.median([d[(s, a)][2] for s in S])), 4)) for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
