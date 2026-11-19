import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S64R', '../S64_構われないと_20261118/走らせる.py')
B, W, N = M.B, M.W, M.N
class 空腹入り(B.換算):
    """Q の入力に空腹 h を1つ足す（つらいのは手のせいでなく空腹だから、を分けられるように）"""
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.Q = np.zeros((W.行動数, W.感覚数 + 2)); s.拡 = None
    def 選ぶ(s, φ):
        s.拡 = np.append(φ, s.h); q = s.Q @ s.拡
        ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        score = q + B.c * max(s.v食, 0.0) * u * ê
        a = int(np.argmax(score))
        if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
        return a, q, ê
    def 受ける(s, φ, a, q, e, 食べた, 我慢=0.0):
        拡 = s.拡; super().受ける(φ, a, q, e, 食べた, 我慢); _, a2, R = s.前; s.前 = (拡, a2, R)
def 一生(s, 入, 欠乏, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = 空腹入り if 入 else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def one(job):
    s, 入, 欠 = job; o = 一生(s, 入, 欠); return (s, 入, 欠, M.P養(o, 7500, 7700), None if 欠 else B.区(o, 7000, 7500)[2])
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(17999, True, True); b = 一生(17999, True, False); c = 一生(17999, False, True)
        print('あり≠なし:', a['sha256'] != c['sha256'], ' 7000まで同じ:', bool((a['行動列'][:7000] == b['行動列'][:7000]).all()), ' なし＝S64:', c['sha256'] == M.一生(17999, '欠乏')['sha256']); sys.exit()
    段 = sys.argv[1]; S = range(17800, 17830) if 段 == '本' else range(17900, 17930)
    with Pool(8) as p: r = p.map(one, [(s, i, e) for i in [False, True] for e in [False, True] for s in S])
    d = {(s, i, e): (p, a) for s, i, e, p, a in r}
    増 = lambda s, i: d[(s, i, True)][0] - d[(s, i, False)][0]
    res = dict(H1_止めずに戻って増える=int(sum(増(s, True) > 0 for s in S)), H2_増えがありで大きい=int(sum(増(s, True) > 増(s, False) for s in S)), H3_普段を壊さない=int(sum(d[(s, True, False)][1] >= 0.9 * d[(s, False, False)][1] for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {f'{"あり" if i else "なし"}': dict(増え=round(float(np.median([増(s, i) for s in S])), 3), P養_なし=round(float(np.median([d[(s, i, False)][0] for s in S])), 3), P養_欠乏=round(float(np.median([d[(s, i, True)][0] for s in S])), 3), 見られ分け=round(float(np.median([d[(s, i, False)][1] for s in S])), 3)) for i in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
