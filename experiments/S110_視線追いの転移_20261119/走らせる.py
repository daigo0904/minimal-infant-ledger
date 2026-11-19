import sys, json, numpy as np
from multiprocessing import Pool
from 共通2 import *
腕 = ['本物', 'ずらし']
def one(job):
    s, a = job; o = 一生(s, 4, a, 学び率=0.01, 視線切替=4000)
    return (s, a) + 追う(o, 3500, 4000) + 追う(o, 4000, 5000) + 追う(o, 7000, 8000) + (float(o['食列'][4000:5000].mean()),)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 26399; o = 一生(s, 4, '本物', 寿命=4600, 学び率=0.01, 視線切替=4000); A, 相, 視, F = o['行動列'], o['相手列'], o['視線列'], o['食列']
        仲 = np.take_along_axis(視, 相, axis=1)
        t = slice(4000, 4600); m = (相[t] > 0) & (A[t] == 仲[t]); n = ~m
        print('4000〜 仲間の視線の手で食べた割合:', round(float(F[t][m].mean()), 3), ' それ以外:', round(float(F[t][n].mean()), 3), '（前が大きければ○）')
        t = slice(3000, 4000); m = (相[t] == 0) & (A[t] == 仲[t]); print('4000 前 養育者の視線の手で食べた割合:', round(float(F[t][m].mean()), 3), ' それ以外:', round(float(F[t][~m].mean()), 3))
        y = [一生(s, 4, a, 寿命=4600, 学び率=0.01, 視線切替=4000)['sha256'] for a in 腕]; print('2腕が違う:', len(set(y)) == 2)
        print('S109 と同じ（切替なしの本物）:', 一生(s, 4, '本物', 寿命=3000, 学び率=0.01)['sha256'] == L('S109共', '../S109_共同注意_20261119/共通2.py').一生(s, 4, '本物', 寿命=3000, 学び率=0.01)['sha256'])
        sys.exit()
    段 = sys.argv[1]; S = range(26200, 26230) if 段 == '本' else range(26300, 26330)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): v for s, a, *v in r}
    res = {'H1_前半に覚えると仲間の視線を早く追う': int(sum(d[(s, '本物')][3] > d[(s, 'ずらし')][3] for s in S)),
           'H2_前半に覚えると邪魔になる': int(sum(d[(s, '本物')][3] < d[(s, 'ずらし')][3] for s in S)),
           'H3_切替後も養育者の視線を追い続ける': int(sum(d[(s, '本物')][2] > d[(s, 'ずらし')][2] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(切替前_養=round(float(np.median([d[(s, a)][0] for s in S])), 3), 切替後1000手_養=round(float(np.median([d[(s, a)][2] for s in S])), 3), 切替後1000手_仲間=round(float(np.median([d[(s, a)][3] for s in S])), 3), 終わり_仲間=round(float(np.median([d[(s, a)][5] for s in S])), 3), 切替後1000手_食べ=round(float(np.median([d[(s, a)][6] for s in S])), 4)) for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
