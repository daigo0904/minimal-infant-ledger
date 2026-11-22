import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S = L('S123選び', '../S123_指す手柄_20261119/選び.py')
def one(job): s, 効 = job; return (s, 効) + S.one((s, 10.0, 効))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 28199; print('効く:', [round(x, 3) for x in one((s, True))[2:]], ' 効かない:', [round(x, 3) for x in one((s, False))[2:]])
        S.A2.設定['窓'] = 3; S.A2.設定['kf'] = 10.0; print('2腕が違う:', S.H.一生(s, 10.0, True, 寿命=2000)['sha256'] != S.H.一生(s, 10.0, False, 寿命=2000)['sha256']); sys.exit()
    段 = sys.argv[1]; R = range(28000, 28030) if 段 == '本' else range(28100, 28130)
    with Pool(8) as p: r = p.map(one, [(s, 効) for 効 in [True, False] for s in R])
    d = {(s, 効): v for s, 効, *v in r}
    res = {'H1_指すのが得な場面で当たりを指す（効く>効かない）': int(sum(d[(s, True)][2] > d[(s, False)][2] for s in R)), 'H2_当たりを指すことが育つ（終わり>初め）': int(sum(d[(s, True)][2] > d[(s, True)][0] for s in R)),
           'H3_食べ物が増える': int(sum(d[(s, True)][4] > d[(s, False)][4] for s in R))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_見ていない時に当たりを指す', '初め_見ている時に取る', '終わり_見ていない時に当たりを指す', '終わり_見ている時に取る', '終わり_食べ']
    res['中央値'] = {('効く' if 効 else '効かない'): {n: round(float(np.median([d[(s, 効)][j] for s in R])), 4) for j, n in enumerate(名)} for 効 in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
