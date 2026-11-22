import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S54R', '../S54_戻ってきた養育者_20261118/走らせる.py')
R, B, W = M.R, M.B, M.W
N = L('S58世界', '../S58_一番の手を除く_20261118/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 形, 寿命=24000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形=形, 切替=8000, 戻り=16000)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
def 一番で合わせて食べた率(o, a, b):
    A, 相, 食, 一 = o['行動列'], o['相手列'], o['食列'], o['一番']; n = m = 0
    for i in range(8):
        t = np.arange(a, b); k = 相[t, i]; 見 = k > 0; t, k = t[見], k[見]
        sel = (A[t, i] == A[t - 1, k - 1]) & (A[t, i] == 一); n += int(sel.sum()); m += int((sel & 食[t, i]).sum())
    return m / max(n, 1)
def one(job):
    s, 形 = job; o = 一生(s, 形)
    return (s, 形, R.数字(o, 23000, 24000), R.数字(o, 15000, 16000), float(o['食列'][8000:16000].mean()))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(15199, '戻る', 10000); b = 一生(15199, '戻る除く', 10000); c = M.一生(15199, 10000)
        print('戻る＝S54:', a['sha256'] == c['sha256'], ' 8000まで同じ:', bool((a['行動列'][:8000] == b['行動列'][:8000]).all()), ' 8000〜で違う:', bool((a['行動列'][8000:] != b['行動列'][8000:]).any()))
        print('一番の手で合わせた時の食べた率 8000〜10000 戻る/戻る除く:', round(一番で合わせて食べた率(a, 8000, 10000), 3), round(一番で合わせて食べた率(b, 8000, 10000), 3), '（基本の給餌 0.01 なら除くは ≈0.01）'); sys.exit()
    段 = sys.argv[1]; S = range(15000, 15030) if 段 == '本' else range(15100, 15130)
    with Pool(8) as p: r = p.map(one, [(s, f) for f in ['戻る', '戻る除く'] for s in S])
    d = {(s, f): (x, y, e) for s, f, x, y, e in r}
    res = dict(H1_漏れが減る=int(sum(d[(s, '戻る除く')][0][2] > -9 and (d[(s, '戻る除く')][0][0] - d[(s, '戻る除く')][0][2]) < (d[(s, '戻る')][0][0] - d[(s, '戻る')][0][2]) for s in S)),
               H2_見られ分けが大きい=int(sum(d[(s, '戻る除く')][0][2] > d[(s, '戻る')][0][2] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f: dict(終_P養合わせ差=[round(float(np.median([d[(s, f)][0][k] for s in S])), 3) for k in range(3)], 終_P他=round(float(np.median([d[(s, f)][0][0] - d[(s, f)][0][2] for s in S])), 3),
                            仲間期末_P養合わせ差=[round(float(np.median([d[(s, f)][1][k] for s in S])), 3) for k in range(3)], 仲間期_食べた=round(float(np.median([d[(s, f)][2] for s in S])), 4)) for f in ['戻る', '戻る除く']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
