import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
sys.path.insert(0, '../S100_多数に合わせる_20261119')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S100R', '../S100_多数に合わせる_20261119/走らせる.py')
R.W.感覚数 = 64; R.N.見た目雑音 = 0.6
def one(job):
    R.W.感覚数 = 64; R.N.見た目雑音 = 0.6; return R.one(job)
腕 = R.腕
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 23999; x = R.しきたりの手(s); o = R.世(s, '流行り', True, '決まった手', 6000)
        print('感覚の W:', R.H.写す(s, 0, '獲得型').感覚.W.shape, '雑音', R.N.見た目雑音)
        for 形 in ['流行り', '仲間へ']:
            A = R.世(s, 形, True, '決まった手')['行動列']; print(形, '8500〜 しきたり 多数:', round(float((A[8500:] == x).mean()), 3))
        y = [R.世(s, 形, 多, 型, 4300)['sha256'] for 形, 多, 型 in 腕]; print('8腕が違う:', len(set(y)) == 8); sys.exit()
    段 = sys.argv[1]; S = range(23800, 23830) if 段 == '本' else range(23900, 23930)
    with Pool(8) as p: r = p.map(one, [(s, 形, 多, 型) for 形, 多, 型 in 腕 for s in S])
    d = {(s, 形, 多, 型): v for s, 形, 多, 型, *v in r}
    効 = lambda s, 形, 多: d[(s, 形, 多, '決まった手')][0] - d[(s, 形, 多, 'でたらめ')][0]
    res = {}
    for 形, 名 in [('流行り', '損'), ('仲間へ', '得')]:
        res[f'H_{名}_多数で残る'] = int(sum(効(s, 形, True) > 0 for s in S)); res[f'H_{名}_多数のほうが残る'] = int(sum(効(s, 形, True) > 効(s, 形, False) for s in S))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{形}_{"多数" if 多 else "写す"}_{型}': dict(しきたり=round(float(np.median([d[(s, 形, 多, 型)][0] for s in S])), 3), 食べ=round(float(np.median([d[(s, 形, 多, 型)][2] for s in S])), 4)) for 形, 多, 型 in 腕}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
