import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
from 共通 import *
代 = dict(しきたり始め=2000, 代替わり=4000, 代替わり間隔=500)
def one(job):
    s, kM, 型 = job; o = 一生(s, 型, True, kM, 寿命=10000, **代); A = o['行動列']; 相 = o['相手列']; x = しきたりの手(s)
    return (s, kM, 型, float((A[8500:10000] == x).mean()), float((A[8500:10000][相[8500:10000] > 0] == x).mean()), float((A[8500:10000] == o['当たり'][0]).mean()), float(o['食列'][8500:10000].mean()))
腕 = [(k, 型) for k in [0.0, 2.0] for 型 in ['でたらめ', '決まった手']]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 23399; x = しきたりの手(s)
        R98 = L('S98R', '../S98_しきたりの代替わり_20261119/走らせる.py')
        print('kM=0 は S98 と同じ sha:', 一生(s, '決まった手', True, 0.0, 寿命=10000, **代)['sha256'] == R98.一生(s, '決まった手', True)['sha256'])
        o = 一生(s, '決まった手', True, 2.0, 寿命=10000, **代); A = o['行動列']
        print('kM=2：2000〜4000 で0〜6 全部しきたり:', bool((A[2000:4000, :7] == x).all()), ' 7500〜 6 が全部しきたりでない:', bool((A[7500:, 6] != x).any()), ' 8500〜 全員のしきたり:', round(float((A[8500:] == x).mean()), 3))
        y = [一生(s, 型, True, k, 寿命=10000, **代)['sha256'] for k, 型 in 腕]; print('4腕が違う:', len(set(y)) == 4); sys.exit()
    段 = sys.argv[1]; S = range(23200, 23230) if 段 == '本' else range(23300, 23330)
    with Pool(8) as p: r = p.map(one, [(s, k, 型) for k, 型 in 腕 for s in S])
    d = {(s, k, 型): v for s, k, 型, *v in r}
    効 = lambda s, k: d[(s, k, '決まった手')][0] - d[(s, k, 'でたらめ')][0]
    res = dict(H1_写す頭で代替わり後も残る=int(sum(効(s, 2.0) > 0 for s in S)), H2_写す頭のほうが残る=int(sum(効(s, 2.0) > 効(s, 0.0) for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_写す頭で代替わり後も残る', 'H2_写す頭のほうが残る']}
    res['中央値'] = {f'kM{k}_{型}': dict(全員のしきたり=round(float(np.median([d[(s, k, 型)][0] for s in S])), 3), 仲間前のしきたり=round(float(np.median([d[(s, k, 型)][1] for s in S])), 3), 当たり=round(float(np.median([d[(s, k, 型)][2] for s in S])), 3), 食べ=round(float(np.median([d[(s, k, 型)][3] for s in S])), 4)) for k, 型 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
