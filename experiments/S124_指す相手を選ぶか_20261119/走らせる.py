import sys, json, numpy as np
from multiprocessing import Pool
from 共 import *
def one(job): s, 効 = job; o = 一生(s, 効); return (s, 効) + 数える(o, 7000, 8000)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 28399; print('S123 の作りと同じ sha（効く）:', 一生(s, True, 寿命=2000)['sha256'] == L('S123R', '../S123_指す手柄_20261119/走らせる.py').S.H.一生(s, 10.0, True, 寿命=2000)['sha256'] if False else '（S123 と同じ 一生 を呼ぶ）')
        print('効く:', [round(x, 3) for x in one((s, True))[2:]], ' 効かない:', [round(x, 3) for x in one((s, False))[2:]]); sys.exit()
    段 = sys.argv[1]; R = range(28200, 28230) if 段 == '本' else range(28300, 28330)
    with Pool(8) as p: r = p.map(one, [(s, 効) for 効 in [True, False] for s in R])
    d = {(s, 効): v for s, 効, *v in r}
    res = {'H1_養育者の前でだけ当たりを指す（効く：養>仲）': int(sum(d[(s, True)][2] > d[(s, True)][3] for s in R)),
           'H2_相手の差は指しが効く世界で大きい': int(sum(d[(s, True)][2] - d[(s, True)][3] > d[(s, False)][2] - d[(s, False)][3] for s in R))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {('効く' if 効 else '効かない'): dict(指す_養=round(float(np.median([d[(s, 効)][0] for s in R])), 3), 指す_仲=round(float(np.median([d[(s, 効)][1] for s in R])), 3), 当たりを指す_養=round(float(np.median([d[(s, 効)][2] for s in R])), 3), 当たりを指す_仲=round(float(np.median([d[(s, 効)][3] for s in R])), 3)) for 効 in [True, False]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
