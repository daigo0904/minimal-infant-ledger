import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S122指頭', '../S122_指さし_20261119/指頭.py'); A2 = L('S122足す2', '../S122_指さし_20261119/足す2.py')
H.食換算 = A2.換算に(H.原換算, H.W, H.B)
def one(job):
    s, 効 = job; A2.設定['窓'] = 3; A2.設定['kf'] = 3.0
    try: o = H.一生(s, 3.0, 効)
    finally: A2.設定['kf'] = 0.0
    return (s, 効) + H.数える(o, 0, 1000) + H.数える(o, 7000, 8000)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 27999; a = one((s, True)); b = one((s, False)); print('効く:', [round(x, 3) for x in a[2:]]); print('効かない:', [round(x, 3) for x in b[2:]])
        A2.設定['窓'] = 3; A2.設定['kf'] = 3.0; print('2腕が違う:', H.一生(s, 3.0, True, 寿命=2000)['sha256'] != H.一生(s, 3.0, False, 寿命=2000)['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(27800, 27830) if 段 == '本' else range(27900, 27930)
    with Pool(8) as p: r = p.map(one, [(s, 効) for 効 in [True, False] for s in S])
    d = {(s, 効): v for s, 効, *v in r}
    res = {'H1_指しが効くと当たりを指す': int(sum(d[(s, True)][4] > d[(s, False)][4] for s in S)), 'H2_指した次に当たりを取る': int(sum(d[(s, True)][6] > d[(s, False)][6] for s in S)),
           'H3_食べ物が増える': int(sum(d[(s, True)][7] > d[(s, False)][7] for s in S)), 'H4_当たりを指すことが育つ': int(sum(d[(s, True)][4] > d[(s, True)][0] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_当たりを指す', '初め_指す', '初め_指した次に取る', '初め_食べ', '終わり_当たりを指す', '終わり_指す', '終わり_指した次に取る', '終わり_食べ']
    res['中央値'] = {('効く' if 効 else '効かない'): {n: round(float(np.nanmedian([d[(s, 効)][j] for s in S])), 4) for j, n in enumerate(名)} for 効 in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
