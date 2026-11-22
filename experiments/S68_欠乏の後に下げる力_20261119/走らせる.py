import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
M = L('S64R', '../S64_構われないと_20261118/走らせる.py')
B, W, N = M.B, M.W, M.N
記録 = {}; 一番 = [0]
class 記す(B.換算):
    """選ぶ時の Q差・つながり項差（一番 − 他の平均）・v食・u・空腹 を記録するだけ"""
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; 記録[i] = []
    def 選ぶ(s, φ):
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ); Lk = B.c * max(s.v食, 0.0) * u * ê; b = 一番[0]
        記録[s.番].append((q[b] - np.delete(q, b).mean(), Lk[b] - np.delete(Lk, b).mean(), s.v食, u, s.h)); return super().選ぶ(φ)
def 一番を調べる(s):
    世 = np.random.default_rng([s, 0]); return int(np.argmax(np.array(W.養育者の好み)[世.permutation(W.行動数)]))
def 一生(s, 欠乏, 記録する=True, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; 記録.clear(); 一番[0] = 一番を調べる(s); N.赤ちゃん = 記す if 記録する else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し='欠乏' if 欠乏 else None)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def one(job):
    s, 欠 = job; o = 一生(s, 欠); assert o['一番'] == 一番[0]
    R = np.array([記録[i] for i in range(8)]).transpose(1, 0, 2); 相 = o['相手列']; m = 相[7500:7700] == 0
    return (s, 欠, [float(R[7500:7700][m][:, k].mean()) for k in range(5)], M.P養(o, 7500, 7700))
名 = ['Q差', 'つながり差', 'v食', 'u', '空腹']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(17199, True); b = 一生(17199, True, False); print('記録しても同じ:', a['sha256'] == b['sha256'], ' 一番一致:', a['一番'] == 一番[0]); sys.exit()
    段 = sys.argv[1]; S = range(17000, 17030) if 段 == '本' else range(17100, 17130)
    with Pool(8) as p: r = p.map(one, [(s, e) for e in [False, True] for s in S])
    d = {(s, e): (v, p) for s, e, v, p in r}
    res = dict(H1_癖が一番の手を下げた=int(sum(d[(s, True)][0][0] < d[(s, False)][0][0] for s in S)), H2_一食の値打ちが上がった=int(sum(d[(s, True)][0][2] > d[(s, False)][0][2] for s in S)),
               H3_つながりが養育者を少し忘れた=int(sum(d[(s, True)][0][3] < d[(s, False)][0][3] for s in S)), 参考_つながり差が下がった=int(sum(d[(s, True)][0][1] < d[(s, False)][0][1] for s in S)))
    res['判定'] = {k: res[k] >= 20 for k in ['H1_癖が一番の手を下げた', 'H2_一食の値打ちが上がった', 'H3_つながりが養育者を少し忘れた']}
    res['中央値'] = {('欠乏' if e else 'なし'): dict({名[k]: round(float(np.median([d[(s, e)][0][k] for s in S])), 4) for k in range(5)}, P養=round(float(np.median([d[(s, e)][1] for s in S])), 3)) for e in [False, True]}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
