import sys, json, numpy as np, importlib.util
sys.path.insert(0, '../S104_同調は増えるか_20261119')
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S104R', '../S104_同調は増えるか_20261119/走らせる.py')
寿命 = 60000
def one(job):
    s, 世界, m = job; o = R.一生(s, 世界, 4, 寿命=寿命, 中立=(m == '中立')); 列 = o['多数列']
    return (s, 世界, m, float(np.mean([n for t, n in 列 if t >= 10000])), float(o['食列'][10000:].mean()))
腕 = R.腕
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 24799; o = R.一生(s, '固定', 4, 寿命=寿命); print('代替わりの回数:', len(o['多数列']), '（(60000−2000)/250=232 なら○）'); print([round(v, 3) for v in one((s, '固定', '選び'))[3:]], [round(v, 3) for v in one((s, '固定', '中立'))[3:]]); sys.exit()
    段 = sys.argv[1]; S = range(24600, 24630) if 段 == '本' else range(24700, 24730)
    with Pool(8) as p: r = p.map(one, [(s, w, m) for w, m in 腕 for s in S])
    d = {(s, w, m): v for s, w, m, *v in r}
    res = {'H_固定_選びで増える': int(sum(d[(s, '固定', '選び')][0] > d[(s, '固定', '中立')][0] for s in S)), 'H_流行り_選びで減る': int(sum(d[(s, '流行り', '選び')][0] < d[(s, '流行り', '中立')][0] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{w}_{m}': dict(同調者=round(float(np.median([d[(s, w, m)][0] for s in S])), 2), 食べ=round(float(np.median([d[(s, w, m)][1] for s in S])), 4)) for w, m in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
