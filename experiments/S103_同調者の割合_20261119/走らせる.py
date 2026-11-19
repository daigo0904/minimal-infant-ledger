import sys, json, numpy as np
sys.path.insert(0, '../S103_同調者の割合_20261119')
from multiprocessing import Pool
from 共通 import *
代 = dict(しきたり始め=2000, 代替わり=4000, 代替わり間隔=500); kM = 5.0
def 世(s, m, 型, 寿命=10000):
    H.設定['多数の子'] = set(range(m))
    try: return 一生(s, 型, True, kM, 寿命=寿命, 形='流行り', **代)
    finally: H.設定['多数の子'] = None
def one(job):
    s, m, 型 = job; o = 世(s, m, 型); A = o['行動列'][8500:]; x = しきたりの手(s); F = o['食列'][8500:]
    return (s, m, 型, float((A == x).mean()), float(F[:, :m].mean()) if m > 0 else None, float(F[:, m:].mean()) if m < 8 else None,
            float((A[:, :m] == x).mean()) if m > 0 else None, float((A[:, m:] == x).mean()) if m < 8 else None)
腕 = [(m, 型) for m in [0, 2, 4, 8] for 型 in ['でたらめ', '決まった手']]
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 24199; R100 = L('S100R', '../S100_多数に合わせる_20261119/走らせる.py')
        print('m=8 は S100 多数と同じ sha:', 世(s, 8, '決まった手', 6000)['sha256'] == R100.世(s, '流行り', True, '決まった手', 6000)['sha256'])
        print('m=0 は S100 写すと同じ sha:', 世(s, 0, '決まった手', 6000)['sha256'] == R100.世(s, '流行り', False, '決まった手', 6000)['sha256'])
        for m in [2, 4]: print(f'm={m}', [None if v is None else round(v, 3) for v in one((s, m, '決まった手'))[3:]])
        y = [世(s, m, 型, 4300)['sha256'] for m, 型 in 腕]; print('8腕が違う:', len(set(y)) == 8); sys.exit()
    段 = sys.argv[1]; S = range(24000, 24030) if 段 == '本' else range(24100, 24130)
    with Pool(8) as p: r = p.map(one, [(s, m, 型) for m, 型 in 腕 for s in S])
    d = {(s, m, 型): v for s, m, 型, *v in r}
    効 = lambda s, m: d[(s, m, '決まった手')][0] - d[(s, m, 'でたらめ')][0]
    res = dict(H1_半分の同調者で残る=int(sum(効(s, 4) > 0 for s in S)), H2_同調者2人では半分より残らない=int(sum(効(s, 2) < 効(s, 4) for s in S)),
               H3_混ざると同調者は食べない=int(sum(d[(s, 4, '決まった手')][1] < d[(s, 4, '決まった手')][2] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    md = lambda xs: None if xs[0] is None else round(float(np.median(xs)), 4)
    res['中央値'] = {f'm{m}_{型}': dict(全員のしきたり=md([d[(s, m, 型)][0] for s in S]), 同調者の食べ=md([d[(s, m, 型)][1] for s in S]), 他の食べ=md([d[(s, m, 型)][2] for s in S]), 同調者のしきたり=md([d[(s, m, 型)][3] for s in S]), 他のしきたり=md([d[(s, m, 型)][4] for s in S])) for m, 型 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
