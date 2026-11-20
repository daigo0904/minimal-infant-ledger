import sys, json, numpy as np
sys.path.insert(0, '../S176_本物のブロッコリー課題_20261120')
from multiprocessing import Pool
from 共 import *
腕 = {'v4_0.05': ('v4', 0.05), 'v4_0': ('v4', 0.0), '元_0.05': ('元', 0.05)}
def one(job):
    s, 名 = job; h, x = 腕[名]; o = 一生(s, h, 二人=0.5, 自分=x); 自 = o['自分手']; A, 相 = o['行動列'][7000:8000], o['相手列'][7000:8000]
    B前自分 = float(np.mean([(A[:, i][相[:, i] == 9] == 自[i]).mean() for i in range(8)]))
    return (s, 名) + ブロッコリー(o, 7000, 8000) + (B前自分, o['sha256'])
if __name__ == '__main__':
    段 = sys.argv[1]; S = list(range(36600, 36630) if 段 == '本' else range(36700, 36730))
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名) for 名 in 腕 for s in S], chunksize=1)
    d = {(s, 名): v for s, 名, *v in r}; assert len(d) == 90
    res = {'H1_自分の好みを持つ': sum(d[(s, 'v4_0.05')][1] > d[(s, 'v4_0')][1] for s in S), 'H2_相手に合わせる': sum(d[(s, 'v4_0.05')][0] > 0 for s in S),
           'H3_相手で切り替える': sum(d[(s, 'v4_0.05')][1] > d[(s, 'v4_0.05')][3] for s in S), '参考_元の自分好きがv4より小さい': sum(d[(s, '元_0.05')][1] < d[(s, 'v4_0.05')][1] for s in S)}
    res['判定'] = {k: res[k] >= 20 for k in ['H1_自分の好みを持つ', 'H2_相手に合わせる', 'H3_相手で切り替える']}
    res['中央値'] = {名: dict(zip(['B前_B好き−自分好き', '仲間前_自分好き', 'A前_A好き−自分好き', 'B前_自分好き'], [round(float(np.median([d[(s, 名)][j] for s in S])), 4) for j in range(4)])) for 名 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
