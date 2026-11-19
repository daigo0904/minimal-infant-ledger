import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S116頭', '../S116_視線は読めるか_20261119/頭.py'); H = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(H)
腕 = [(0.0, '本物'), (3.0, '本物'), (3.0, 'ずらし')]
def one(job):
    s, kf, a = job; o = H.一生(s, kf, a)
    return (s, kf, a) + H.持ち上がり(o, 0, 1000) + H.持ち上がり(o, 7000, 8000) + H.持ち上がり(o, 7000, 8000, 相手=1) + (float(o['食列'][7000:].mean()),)
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 27199; print('kf=0 は S109 と同じ sha:', H.一生(s, 0.0)['sha256'] == H.C.一生(s, 4, '本物', 学び率=0.01)['sha256'])
        y = [H.一生(s, kf, a, 寿命=2000)['sha256'] for kf, a in 腕]; print('3腕が違う:', len(set(y)) == 3)
        print({f'{kf}_{a}': [round(v, 3) for v in one((s, kf, a))[3:]] for kf, a in 腕}); sys.exit()
    段 = sys.argv[1]; S = range(27000, 27030) if 段 == '本' else range(27100, 27130)
    with Pool(8) as p: r = p.map(one, [(s, kf, a) for kf, a in 腕 for s in S])
    d = {(s, kf, a): v for s, kf, a, *v in r}
    res = {'H1_真ん中の手も追う（kf3>kf0）': int(sum(d[(s, 3.0, '本物')][3] > d[(s, 0.0, '本物')][3] for s in S)),
           'H2_真ん中の手で育つ（終わり>初め）': int(sum(d[(s, 3.0, '本物')][3] > d[(s, 3.0, '本物')][1] for s in S)),
           'H3_ずらしでは追わない（本物>ずらし）': int(sum(d[(s, 3.0, '本物')][3] > d[(s, 3.0, 'ずらし')][3] for s in S))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['初め_端', '初め_真ん中', '終わり_端', '終わり_真ん中', '終わり_仲間_端', '終わり_仲間_真ん中', '食べ']
    res['中央値'] = {f'kf{kf}_{a}': {n: round(float(np.median([d[(s, kf, a)][j] for s in S])), 3) for j, n in enumerate(名)} for kf, a in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
