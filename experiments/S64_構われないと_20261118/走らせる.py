import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # 換算型（c=30）と S16 世界（感覚256・雑音0.3）
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
N = L('S64世界', '../S64_構われないと_20261118/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
W = B.W
def 一生(s, 腕, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 腕 == '欠乏' else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def P養(o, a, b):
    A, 相, 一 = o['行動列'], o['相手列'], o['一番']; return float(np.mean([(A[a:b, i][相[a:b, i] == 0] == 一).mean() for i in range(8)]))
def one(job):
    s, 腕 = job; o = 一生(s, 腕)
    return (s, 腕, P養(o, 7500, 7700), float(o['h列'][75:77].mean()), P養(o, 6800, 7000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(16299, '欠乏'); b = 一生(16299, 'なし')
        print('7000まで同じ:', bool((a['行動列'][:7000] == b['行動列'][:7000]).all()), ' 欠乏中に養育者が見る手:', int((a['相手列'][7000:7500] == 0).sum()), ' なしでは:', int((b['相手列'][7000:7500] == 0).sum()))
        sp = importlib.util.spec_from_file_location('S47R', '../S47_本物とずらし_20261118/走らせる.py'); Z = importlib.util.module_from_spec(sp); sp.loader.exec_module(Z)
        print('なし＝S47 の本物:', b['sha256'] == Z.一生(16299, '本物')['sha256'])
        print('欠乏中の食べた割合 あり/なし:', round(float(a['食列'][7000:7500].mean()), 4), round(float(b['食列'][7000:7500].mean()), 4)); sys.exit()
    段 = sys.argv[1]; S = range(16200, 16230) if 段 == '本' else range(16300, 16330)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['なし', '欠乏'] for s in S])
    d = {(s, a): (x, h, x0) for s, a, x, h, x0 in r}
    res = dict(H1_戻って喜ばせが増える=int(sum(d[(s, '欠乏')][0] > d[(s, 'なし')][0] for s in S)), H2_空腹が高い=int(sum(d[(s, '欠乏')][1] > d[(s, 'なし')][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(P養_7500=round(float(np.median([d[(s, a)][0] for s in S])), 3), 空腹=round(float(np.median([d[(s, a)][1] for s in S])), 3), P養_6800=round(float(np.median([d[(s, a)][2] for s in S])), 3)) for a in ['なし', '欠乏']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
