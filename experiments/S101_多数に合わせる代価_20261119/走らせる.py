import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
C = L('S100共通', '../S100_多数に合わせる_20261119/共通.py')
H, B, W, N, K = C.H, C.B, C.W, C.N, C.K
頭 = {'換算': (0.0, False), '写す': (5.0, False), '多数': (5.0, True)}
def 一生(s, 名, 寿命=10000):
    kM, 多数 = 頭[名]
    W.学び率 = 0.05; B.v時定数 = 5000.0; N.行動数 = K; W.行動数 = K; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9] + [-0.5] * 12; W.見た目次元 = 8 + K + 1; N.赤ちゃん = H.写す; H.設定['kM'] = kM; H.設定['多数'] = 多数
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='流行り', 食べた見える=True)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8; H.設定['kM'] = 0.0; H.設定['多数'] = False
def one(job):
    s, 名 = job; o = 一生(s, 名); A = o['行動列']; 当 = np.array(o['当たり'])[np.arange(len(A)) // 1000][:, None]
    切 = np.mean([(A[t:t + 200] == 当[t:t + 200]).mean() for t in range(2000, 10000, 1000)])
    前当 = np.array(o['当たり'])[np.maximum(np.arange(len(A)) // 1000 - 1, 0)][:, None]
    古 = np.mean([(A[t:t + 200] == 前当[t:t + 200]).mean() for t in range(2000, 10000, 1000)])
    c = np.bincount(A[2000:].ravel(), minlength=K) / A[2000:].size
    return (s, 名, float(o['食列'][2000:].mean()), float(切), float(古), float((A[2000:] == 当[2000:]).mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 23799; y = {名: 一生(s, 名, 4300)['sha256'] for 名 in 頭}; print('3腕が違う:', len(set(y.values())) == 3)
        for 名 in 頭: print(名, [round(x, 3) for x in one((s, 名))[2:]])
        sys.exit()
    段 = sys.argv[1]; S = range(23600, 23630) if 段 == '本' else range(23700, 23730)
    with Pool(8) as p: r = p.map(one, [(s, 名) for 名 in 頭 for s in S])
    d = {(s, 名): v for s, 名, *v in r}
    res = dict(H1_多数は写すより食べない=int(sum(d[(s, '多数')][0] < d[(s, '写す')][0] for s in S)), H2_多数は換算より食べない=int(sum(d[(s, '多数')][0] < d[(s, '換算')][0] for s in S)),
               H3_多数は切り替え直後に新しい当たりが少ない=int(sum(d[(s, '多数')][1] < d[(s, '写す')][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {名: dict(食べ=round(float(np.median([d[(s, 名)][0] for s in S])), 4), 切替直後の新しい当たり=round(float(np.median([d[(s, 名)][1] for s in S])), 3), 切替直後の古い当たり=round(float(np.median([d[(s, 名)][2] for s in S])), 3), 当たり=round(float(np.median([d[(s, 名)][3] for s in S])), 3)) for 名 in 頭}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
