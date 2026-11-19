import sys, json, numpy as np
from multiprocessing import Pool
from 共通2 import *
K = 4; 腕 = ['本物', 'ずらし', '見えない']
def one(job):
    s, a = job; o = 一生(s, K, a, 学び率=0.01)
    return (s, a) + 追う(o, 0, 500) + 追う(o, 7000, 8000) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 26199; o = 一生(s, K, '本物', 寿命=2000, 学び率=0.01)
        print('視線列の形:', o['視線列'].shape, '（2000, 9）', ' 感覚の入力の大きさ:', W.見た目次元 if False else 8 + K + 1 + K)
        R106 = L('S106共通', '../S106_世界の変わりやすさと同調_20261119/共通.py')
        y = [一生(s, K, a, 寿命=2000, 学び率=0.01)['sha256'] for a in 腕]; print('3腕が違う:', len(set(y)) == 3)
        print('1世界の8000手:', {a: [round(v, 3) for v in one((s, a))[2:]] for a in 腕}); sys.exit()
    段 = sys.argv[1]; S = range(26000, 26030) if 段 == '本' else range(26100, 26130)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in 腕 for s in S])
    d = {(s, a): v for s, a, *v in r}
    res = {'H1_視線を追うことが育つ': int(sum(d[(s, '本物')][2] > d[(s, '本物')][0] for s in S)), 'H2_養育者の視線だけ追う': int(sum(d[(s, '本物')][2] > d[(s, '本物')][3] for s in S)),
           'H3_本物はずらしより追う': int(sum(d[(s, '本物')][2] > d[(s, 'ずらし')][2] for s in S)), 'H4_本物は見えないより食べる': int(sum(d[(s, '本物')][4] > d[(s, '見えない')][4] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(初め_養=round(float(np.median([d[(s, a)][0] for s in S])), 3), 初め_他=round(float(np.median([d[(s, a)][1] for s in S])), 3), 終わり_養=round(float(np.median([d[(s, a)][2] for s in S])), 3), 終わり_他=round(float(np.median([d[(s, a)][3] for s in S])), 3), 食べ=round(float(np.median([d[(s, a)][4] for s in S])), 4)) for a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
