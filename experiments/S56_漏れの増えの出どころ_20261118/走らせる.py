import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S54R', '../S54_戻ってきた養育者_20261118/走らせる.py')
R, B, W, N = M.R, M.B, M.W, M.N
窓 = [None]; 記録 = {}
class 診る(B.換算):
    """窓[0]=(lo,hi) の手だけつながりの項を切る。毎手 u を記録（行動は変えない）"""
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.手数 = 0; s.番 = i; 記録[i] = []
    def 選ぶ(s, φ):
        s.手数 += 1; 記録[s.番].append(s.つながり.予測(φ))
        if 窓[0] and 窓[0][0] < s.手数 <= 窓[0][1]:
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); a = int(np.argmax(q))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        return super().選ぶ(φ)
def 一生(s, 腕, 切, 寿命=24000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = 診る; 窓[0] = 切; 記録.clear()
    try:
        if 腕 == '戻る': return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='戻る', 切替=8000, 戻り=16000)
        return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8; 窓[0] = None
def P他(o, a, b):
    A, 相, 一 = o['行動列'], o['相手列'], o['一番']; return float(np.mean([(A[a:b, i][相[a:b, i] > 0] == 一).mean() for i in range(8)]))
def one(job):
    s, 腕 = job
    A = 一生(s, 腕, None); U = np.array([記録[i] for i in range(8)]).T; 相 = A['相手列']
    u他 = float(np.mean([U[23000:24000, i][相[23000:24000, i] > 0].mean() for i in range(8)]))
    C = 一生(s, 腕, (23000, 24000)); assert (A['行動列'][:23000] == C['行動列'][:23000]).all()
    return (s, 腕, u他, P他(A, 23000, 24000), P他(C, 23000, 24000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(14799, '戻る', None, 23300); c = M.一生(14799, 23300); b = 一生(14799, '戻る', (23000, 24000), 23300)
        print('記録しても S54 と同じ:', a['sha256'] == c['sha256'], ' 23000まで同じ:', bool((a['行動列'][:23000] == b['行動列'][:23000]).all()), ' 23000〜で違う:', bool((a['行動列'][23000:] != b['行動列'][23000:]).any())); sys.exit()
    段 = sys.argv[1]; S = range(14600, 14630) if 段 == '本' else range(14700, 14730)
    with Pool(8) as p: r = p.map(one, [(s, a) for a in ['ずっと', '戻る'] for s in S])
    d = {(s, a): (u, p0, p1) for s, a, u, p0, p1 in r}
    res = dict(H1_仲間へのつながりが残る=int(sum(d[(s, '戻る')][0] > d[(s, 'ずっと')][0] for s in S)),
               H2_切ると漏れの差が縮む=int(sum(d[(s, '戻る')][2] - d[(s, 'ずっと')][2] < d[(s, '戻る')][1] - d[(s, 'ずっと')][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {a: dict(u他=round(float(np.median([d[(s, a)][0] for s in S])), 4), P他_切らない=round(float(np.median([d[(s, a)][1] for s in S])), 3), P他_切る=round(float(np.median([d[(s, a)][2] for s in S])), 3)) for a in ['ずっと', '戻る']}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
