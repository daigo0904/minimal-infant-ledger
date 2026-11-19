import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
G = L('S127重み', '../S127_癖の重み_20261119/重み.py')
H = L('S125叙頭', '../S125_叙述的指さし_20261119/叙頭.py'); H.食換算 = G.に(H.原換算, H.W, H.B)
腕 = [(1.0, '褒める'), (0.2, '褒める'), (0.2, '褒めない')]
def one(job):
    s, λ, 叙 = job; G.設定['λ'] = λ
    try: o = H.一生(s, 叙)
    finally: G.設定['λ'] = 1.0
    return (s, λ, 叙) + H.指す(o, 0, 1000) + H.指す(o, 7000, 8000)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 28999; 元 = L('S125元', '../S125_叙述的指さし_20261119/叙頭.py')
        print('λ=1 は S125 と同じ sha:', (lambda: (G.設定.update(λ=1.0), H.一生(s, '褒める', 寿命=1500)['sha256'])[1])() == 元.一生(s, '褒める', 寿命=1500)['sha256'])
        G.設定['λ'] = 0.2; print('λ=0.2 で手が変わる:', H.一生(s, '褒める', 寿命=1500)['sha256'] != 元.一生(s, '褒める', 寿命=1500)['sha256']); G.設定['λ'] = 1.0
        print({f'{λ}_{叙}': [round(x, 3) for x in one((s, λ, 叙))[3:]] for λ, 叙 in 腕}); sys.exit()
    段 = sys.argv[1]; R = range(28800, 28830) if 段 == '本' else range(28900, 28930)
    with Pool(8) as p: r = p.map(one, [(s, λ, 叙) for λ, 叙 in 腕 for s in R])
    d = {(s, λ, 叙): v for s, λ, 叙, *v in r}
    res = {'H1_λ0.2 で指すことが育つ（終わり>初め）': int(sum(d[(s, 0.2, '褒める')][3] > d[(s, 0.2, '褒める')][0] for s in R)),
           'H2_λ0.2 のほうが指す（λ1 と比べる）': int(sum(d[(s, 0.2, '褒める')][3] > d[(s, 1.0, '褒める')][3] for s in R)),
           'H3_育つのは褒めのおかげ（λ0.2 褒める>褒めない）': int(sum(d[(s, 0.2, '褒める')][3] > d[(s, 0.2, '褒めない')][3] for s in R))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_養育者の前で指す', '初め_仲間の前', '初め_食べ', '終わり_養育者の前で指す', '終わり_仲間の前', '終わり_食べ']
    res['中央値'] = {f'λ{λ}_{叙}': {n: round(float(np.median([d[(s, λ, 叙)][j] for s in R])), 4) for j, n in enumerate(名)} for λ, 叙 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
