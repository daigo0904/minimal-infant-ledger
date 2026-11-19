import sys, json, numpy as np
from multiprocessing import Pool
from 共 import *
J48 = [('本物', 3.0), ('ずらし', 3.0), ('道具', 0.0)]; J100 = [('決まった手', 3.0), ('でたらめ', 3.0)]
def a(job): s, 腕, kf = job; return ('48', s, 腕) + 見られ分け(s, 腕, kf)[1:]
def b(job): s, 型, kf = job; return ('100', s, 型, しきたり(s, True, 型, kf)[1])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 27599; A.設定['kf'] = 0.0
        print('S48 kf0 は元と同じ sha（本物・ずらし）:', all(見られ分け(s, 腕, 0.0, 1500)[0]['sha256'] == L(f'S48元{腕}', '../S48_得と邪魔を分ける_20261118/走らせる.py').一生(s, 腕, 1500)['sha256'] for 腕 in ['本物', 'ずらし']))
        print('S100 kf0 は元と同じ sha:', しきたり(s, True, '決まった手', 0.0, 3000)[0]['sha256'] == L('S100元', '../S100_多数に合わせる_20261119/走らせる.py').世(s, '流行り', True, '決まった手', 3000)['sha256'])
        print('kf3 で手が変わる:', 見られ分け(s, '本物', 3.0, 1500)[0]['sha256'] != 見られ分け(s, '本物', 0.0, 1500)[0]['sha256'], しきたり(s, True, '決まった手', 3.0, 3000)[0]['sha256'] != しきたり(s, True, '決まった手', 0.0, 3000)[0]['sha256'])
        sys.exit()
    段 = sys.argv[1]; S = range(27400, 27430) if 段 == '本' else range(27500, 27530)
    with Pool(8) as p: r = p.map(a, [(s, 腕, kf) for 腕, kf in J48 for s in S]) + p.map(b, [(s, 型, kf) for 型, kf in J100 for s in S])
    d = {(x[0], x[1], x[2]): x[3:] for x in r}
    res = {'H1_食べ予測でも本物>ずらし（S48の芯）': int(sum(d[('48', s, '本物')][1] > d[('48', s, 'ずらし')][1] for s in S)),
           'H2_食べ予測でもしきたりが残る（S100の芯）': int(sum(d[('100', s, '決まった手')][0] > d[('100', s, 'でたらめ')][0] for s in S)),
           'H3_食べ予測でもずらし<道具（S48の邪魔）': int(sum(d[('48', s, 'ずらし')][1] < d[('48', s, '道具')][1] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {**{f'S48_{腕}': [round(float(np.median([d[('48', s, 腕)][k] for s in S])), 3) for k in range(2)] for 腕, _ in J48}, **{f'S100_{型}': round(float(np.median([d[('100', s, 型)][0] for s in S])), 3) for 型, _ in J100}}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
