import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S125叙頭', '../S125_叙述的指さし_20261119/叙頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
def one(job): s, 叙 = job; o = H.一生(s, 叙); return (s, 叙) + H.指す(o, 0, 1000) + H.指す(o, 7000, 8000)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 28599; print({a: [round(x, 3) for x in one((s, a))[2:]] for a in ['褒める', '褒めない']}); sys.exit()
    段 = sys.argv[1]; R = range(28400, 28430) if 段 == '本' else range(28500, 28530)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['褒める', '褒めない'] for s in R])
    d = {(s, a): v for s, a, *v in r}
    res = {'H1_褒められると養育者の前で指す': int(sum(d[(s, '褒める')][3] > d[(s, '褒めない')][3] for s in R)), 'H2_食べ物を損してでも指す（褒めるの食べが少ない）': int(sum(d[(s, '褒める')][5] < d[(s, '褒めない')][5] for s in R)),
           'H3_指すことが育つ（褒める：終わり>初め）': int(sum(d[(s, '褒める')][3] > d[(s, '褒める')][0] for s in R))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_養育者の前で指す', '初め_仲間の前で指す', '初め_食べ', '終わり_養育者の前で指す', '終わり_仲間の前で指す', '終わり_食べ']
    res['中央値'] = {a: {n: round(float(np.median([d[(s, a)][j] for s in R])), 4) for j, n in enumerate(名)} for a in ['褒める', '褒めない']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
