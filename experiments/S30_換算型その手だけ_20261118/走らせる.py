import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def 読む(名, path):
    sp = importlib.util.spec_from_file_location(名, path); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); m.感覚数 = 256; m.見た目雑音 = 0.3; return m
W = 読む('S16世界', '../S16_気に入りを持ち越さない_20261118/世界.py')
原 = W.赤ちゃん
c = 30.0; v時定数 = 1000.0
class 換算(原):
    """S28 頭.py の換算型と同じ中身を S16 の世界の赤ちゃんの上に作る"""
    def __init__(s, 種, i, 頭):
        super().__init__(種, i, 頭); s.v食 = s.v有 = s.v無 = 0.0; s.前食 = None
    def 選ぶ(s, φ):
        q = s.Q @ φ
        ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + c * max(s.v食, 0.0) * u * ê
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        if s.前 is not None and s.前食 is not None:
            φp, ap, Rp = s.前; δ = Rp + W.割引 * q[a] - s.Q[ap] @ φp
            if s.前食: s.v有 += (δ - s.v有) / v時定数
            else: s.v無 += (δ - s.v無) / v時定数
            s.v食 = s.v有 - s.v無
        super().受ける(φ, a, q, e, 食べた, 我慢); s.前食 = 食べた
def 一生(s, 形, 寿命=8000):
    W.赤ちゃん = 換算
    try: return W.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形=形)
    finally: W.赤ちゃん = 原
def 区(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    pa = np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]); po = np.mean([(A[lo:hi, i][相[lo:hi, i] > 0] == b).mean() for i in range(8)])
    return [float(pa), float(po), float(pa - po)]
def one(job):
    s, 形 = job; o = 一生(s, 形)
    return (s, 形, 区(o, 0, 500), [float(np.mean([区(o, 7000, 7500)[k], 区(o, 7500, 8000)[k]])) for k in range(3)])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        sys.path.insert(0, '../S28_換算型_20261118'); import 頭 as H
        H.c[0] = 30.0; a = 一生(9499, '持ち越す', 600); b = 一生(9499, 'その手だけ', 600); r = H.一生(9499, '獲得型', 換算する=True, 寿命=600)
        print('持ち越す＝S28 換算型:', a['sha256'] == r['sha256'], ' 持ち越す≠その手だけ:', a['sha256'] != b['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(9400, 9410) if 段 == '本' else range(9500, 9510)
    with Pool(8) as p: r = p.map(one, [(s, 形) for 形 in ['持ち越す', 'その手だけ'] for s in S])
    d = {(s, 形): (f, g) for s, 形, f, g in r}
    res = dict(H1_漏れが減る=int(sum(d[(s, 'その手だけ')][1][1] < d[(s, '持ち越す')][1][1] for s in S)),
               H2_見られ分けが大きい=int(sum(d[(s, 'その手だけ')][1][2] > d[(s, '持ち越す')][1][2] for s in S)),
               H3_育ちで出る=int(sum(d[(s, 'その手だけ')][0][2] <= d[(s, 'その手だけ')][1][2] / 2 for s in S)))
    res['判定'] = {k: v >= 8 for k, v in res.items()}
    res['中央値_P養P他差'] = {f'{形}_{w}': [round(float(np.median([d[(s, 形)][j][k] for s in S])), 3) for k in range(3)] for 形 in ['持ち越す', 'その手だけ'] for j, w in enumerate(['初め', '育'])}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
