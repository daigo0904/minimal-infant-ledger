import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
from 共通 import *
代 = dict(しきたり始め=2000, 代替わり=4000, 代替わり間隔=500); kM = 5.0
def 世(s, 形, 多数, 型, 寿命=10000):
    kw = dict(代, 切替=0) if 形 == '仲間へ' else dict(代)
    return 一生(s, 型, True, kM, 寿命=寿命, 多数=多数, 形=形, **kw)
def one(job):
    s, 形, 多数, 型 = job; o = 世(s, 形, 多数, 型); A = o['行動列']; x = しきたりの手(s); c = np.bincount(A[8500:].ravel(), minlength=K) / A[8500:].size
    return (s, 形, 多数, 型, float((A[8500:] == x).mean()), float(c.max()), float(o['食列'][8500:].mean()))
腕 = [(形, 多数, 型) for 形 in ['流行り', '仲間へ'] for 多数 in [False, True] for 型 in ['でたらめ', '決まった手']]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 23599; x = しきたりの手(s)
        R99 = L('S99共通', '../S99_写し取りの強さ_20261119/共通.py')
        print('多数=False は S99 の写す頭と同じ sha:', 世(s, '流行り', False, '決まった手', 6000)['sha256'] == R99.一生(s, '決まった手', True, kM, 寿命=6000, **代)['sha256'])
        for 形 in ['流行り', '仲間へ']:
            o = 世(s, 形, True, '決まった手'); A = o['行動列']
            print(形, '2000〜4000 0〜6 全部しきたり:', bool((A[2000:4000, :7] == x).all()), ' 7500〜 6 全部しきたりでない:', bool((A[7500:, 6] != x).any()), ' 8500〜 全員のしきたり:', round(float((A[8500:] == x).mean()), 3))
        y = [世(s, 形, 多, 型, 4300)['sha256'] for 形, 多, 型 in 腕]; print('8腕が違う:', len(set(y)) == 8); sys.exit()
    段 = sys.argv[1]; S = range(23400, 23430) if 段 == '本' else range(23500, 23530)
    with Pool(8) as p: r = p.map(one, [(s, 形, 多, 型) for 形, 多, 型 in 腕 for s in S])
    d = {(s, 形, 多, 型): v for s, 形, 多, 型, *v in r}
    効 = lambda s, 形, 多: d[(s, 形, 多, '決まった手')][0] - d[(s, 形, 多, 'でたらめ')][0]
    res = {}
    for 形, 名 in [('流行り', '損'), ('仲間へ', '得')]:
        res[f'H_{名}_多数で残る'] = int(sum(効(s, 形, True) > 0 for s in S)); res[f'H_{名}_多数のほうが残る'] = int(sum(効(s, 形, True) > 効(s, 形, False) for s in S))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{形}_{"多数" if 多 else "写す"}_{型}': dict(しきたり=round(float(np.median([d[(s, 形, 多, 型)][0] for s in S])), 3), 一番多い手=round(float(np.median([d[(s, 形, 多, 型)][1] for s in S])), 3), 食べ=round(float(np.median([d[(s, 形, 多, 型)][2] for s in S])), 4)) for 形, 多, 型 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
