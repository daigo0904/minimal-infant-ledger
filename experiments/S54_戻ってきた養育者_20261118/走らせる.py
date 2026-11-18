import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S50R', '../S50_相手の直前の手が見える_20261118/走らせる.py')   # 本物の頭と数え方
B, W = R.B, R.W
N = L('S54世界', '../S54_戻ってきた養育者_20261118/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 寿命=24000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='戻る', 切替=8000, 戻り=16000)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 区列(o, a, b): return [B.区(o, k, k + 500)[2] for k in range(a, b, 500)]
def 初超え(列, 線=0.3):
    for k, x in enumerate(列):
        if x > 線: return k
    return 99
def one(s):
    o = 一生(s); 生 = 区列(o, 0, 8000); 戻 = 区列(o, 16000, 24000)
    return dict(種=s, 生=生, 戻=戻, 直前=R.数字(o, 15000, 16000), 食=[float(o['食列'][a:a + 1000].mean()) for a in (7000, 15000, 16000, 23000)])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(14399, 17000); c = R.一生(14399, '替える', 17000)   # 世界の乱数は寿命で決まるので同じ寿命で比べる
        print('16000手まで S50 替えると同じ:', bool((o['行動列'][:16000] == c['行動列'][:16000]).all()), ' 16000〜で違う:', bool((o['行動列'][16000:] != c['行動列'][16000:]).any()), ' 食べた割合 7000〜8000/15000〜16000/16000〜17000:', [round(float(o['食列'][a:a + 1000].mean()), 4) for a in (7000, 15000, 16000)]); sys.exit()
    段 = sys.argv[1]; S = range(14200, 14230) if 段 == '本' else range(14300, 14330)
    with Pool(8) as p: rows = p.map(one, list(S))
    res = dict(H1_初めより高く戻る=int(sum(r['戻'][0] > r['生'][0] for r in rows)), H2_学び直しが速い=int(sum(初超え(r['戻']) < 初超え(r['生']) for r in rows)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = dict(生=[round(float(np.median([r['生'][k] for r in rows])), 3) for k in range(16)], 戻=[round(float(np.median([r['戻'][k] for r in rows])), 3) for k in range(16)],
                       超える区間_生=float(np.median([初超え(r['生']) for r in rows])), 超える区間_戻=float(np.median([初超え(r['戻']) for r in rows])), 直前_P養合わせ差=[round(float(np.median([r['直前'][k] for r in rows])), 3) for k in range(3)],
                       食べた割合=[round(float(np.median([r['食'][k] for r in rows])), 4) for k in range(4)])
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
