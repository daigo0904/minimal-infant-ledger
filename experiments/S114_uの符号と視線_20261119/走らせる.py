import sys, json, numpy as np, importlib.util
sys.path.insert(0, '../S109_共同注意_20261119')
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S113R', '../S113_視線追いの仕組み_20261119/走らせる.py')
def one(s, lo=7000, hi=8000):
    o, Rec = R.一生(s); 相, 視, A = o['相手列'], o['視線列'], o['行動列']; 好 = np.array(o['好み']); 中 = 好 - 好.mean()
    順 = np.argsort(好); 端 = {int(順[0]), int(順[-1])}
    相関, 端追, 中追 = [], [], []
    for i in range(8):
        m = np.arange(lo, hi)[相[lo:hi, i] == 0]; g = 視[m, 0]; U = Rec[i]['u'][m]
        相関.append(float(np.corrcoef(U, 中[g])[0, 1]))
        e = np.array([x in 端 for x in g]); 追 = A[m, i] == g
        端追.append(float(追[e].mean())); 中追.append(float(追[~e].mean()))
    return (s, float(np.mean(相関)), float(np.mean(端追)), float(np.mean(中追)))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 26999; o, Rec = R.一生(s); print('好み:', o['好み'], ' 記録の u が動く:', round(float(Rec[0]['u'][7000:8000].std()), 4))
        print('1世界（u と 好み[視線]−平均 の相関、端の手を追う、真ん中の手を追う）:', [round(v, 3) for v in one(s)[1:]]); sys.exit()
    段 = sys.argv[1]; S = range(26800, 26830) if 段 == '本' else range(26900, 26930)
    with Pool(8) as p: r = p.map(one, list(S))
    res = {'H1_uの符号が視線の手の好みと組む': int(sum(x[1] > 0 for x in r)), 'H2_端の好みの手ほど強く追う': int(sum(x[2] > x[3] for x in r))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = dict(相関=round(float(np.median([x[1] for x in r])), 3), 端の手を追う=round(float(np.median([x[2] for x in r])), 3), 真ん中の手を追う=round(float(np.median([x[3] for x in r])), 3))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
