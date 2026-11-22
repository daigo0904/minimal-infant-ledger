import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S54R', '../S54_戻ってきた養育者_20261118/走らせる.py')
def 割合(o, a, b):
    """他の子が見ていて、その子の直前の手に合わせ、食べ物が出た手のうち、養育者の一番好きな手の割合（8人分まとめて）"""
    A, 相, 食, 一 = o['行動列'], o['相手列'], o['食列'], o['一番']
    n = m = 0
    for i in range(8):
        t = np.arange(max(a, 1), b); k = 相[t, i]; 見 = k > 0
        t, k = t[見], k[見]
        合 = A[t, i] == A[t - 1, k - 1]
        ok = 合 & 食[t, i]
        n += int(ok.sum()); m += int((ok & (A[t, i] == 一)).sum())
    return m / max(n, 1), n
def one(s):
    o = M.一生(s); return (s, 割合(o, 8000, 10000), 割合(o, 14000, 16000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = M.一生(14899, 10000); A, 相, 食, 一 = o['行動列'], o['相手列'], o['食列'], o['一番']
        # 手で数える：1人目だけ、素朴なループで
        n = m = 0
        for t in range(8000, 10000):
            k = 相[t, 0]
            if k > 0 and A[t, 0] == A[t - 1, k - 1] and 食[t, 0]:
                n += 1; m += int(A[t, 0] == 一)
        f = 割合(dict(行動列=A[:, :1].repeat(8, 1) * 0 + A[:, :1], 相手列=相, 食列=食, 一番=一), 8000, 10000) if False else None
        # 関数版を1人目だけに絞って比べる
        A2 = A.copy(); 相2 = 相.copy(); 相2[:, 1:] = 0
        g, n2 = 割合(dict(行動列=A2, 相手列=相2, 食列=食, 一番=一), 8000, 10000)
        print('手で数えた 1人目:', m, '/', n, ' 関数で:', round(g * n2), '/', n2, ' 一致:', (m, n) == (round(g * n2), n2)); sys.exit()
    段 = sys.argv[1]; S = range(14800, 14830) if 段 == '本' else range(14900, 14930)
    with Pool(8) as p: r = p.map(one, list(S))
    res = dict(H1_合わせて食べた手は一番の手が多い=int(sum(x[1][0] > 0.4 for x in r)), H2_だんだん散る=int(sum(x[1][0] > x[2][0] for x in r)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = dict(割合_8000=round(float(np.median([x[1][0] for x in r])), 3), 割合_14000=round(float(np.median([x[2][0] for x in r])), 3), 数_8000=int(np.median([x[1][1] for x in r])), 数_14000=int(np.median([x[2][1] for x in r])))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
