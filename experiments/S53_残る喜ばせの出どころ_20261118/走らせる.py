import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S50R', '../S50_相手の直前の手が見える_20261118/走らせる.py')   # S50 の世界（12次元入力・仲間へ）と本物の頭
B, W, N = R.B, R.W, R.N
窓 = [None]; 記録 = {}
class 診る(B.換算):
    """窓[0]=(lo,hi) の手だけつながりの項を切って Q だけで選ぶ。毎手 u を記録（行動は変えない）"""
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.手数 = 0; s.番 = i; 記録[i] = []
    def 選ぶ(s, φ):
        s.手数 += 1; 記録[s.番].append(s.つながり.予測(φ))
        if 窓[0] and 窓[0][0] < s.手数 <= 窓[0][1]:
            q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); a = int(np.argmax(q))
            if s.手.random() < W.探る: a = int(s.手.integers(W.行動数))
            return a, q, ê
        return super().選ぶ(φ)
def 一生(s, 切, 寿命=16000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; W.見た目次元 = 12; N.赤ちゃん = 診る; 窓[0] = 切; 記録.clear()
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='仲間へ', 切替=8000)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8; 窓[0] = None
def u養(U, 相, a, b): return float(np.mean([U[a:b, i][相[a:b, i] == 0].mean() for i in range(8)]))
def one(s):
    A = 一生(s, None); U = np.array([記録[i] for i in range(8)]).T
    C = 一生(s, (15000, 16000)); assert (A['行動列'][:15000] == C['行動列'][:15000]).all()
    相 = A['相手列']
    return (s, R.数字(A, 15000, 16000)[0], R.数字(C, 15000, 16000)[0], u養(U, 相, 7000, 8000), u養(U, 相, 15000, 16000))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(14199, None, 15300); b = 一生(14199, (15000, 16000), 15300); c = R.一生(14199, '替える', 15300)
        print('記録しても S50 替えると同じ:', a['sha256'] == c['sha256'], ' 15000まで同じ:', bool((a['行動列'][:15000] == b['行動列'][:15000]).all()), ' 15000〜で違う:', bool((a['行動列'][15000:] != b['行動列'][15000:]).any())); sys.exit()
    段 = sys.argv[1]; S = range(14000, 14030) if 段 == '本' else range(14100, 14130)
    with Pool(8) as p: r = p.map(one, list(S))
    res = dict(H1_切ると喜ばせが消える=int(sum(c < 0.6 * a for _, a, c, _, _ in r)), H2_まだ養育者を覚えている=int(sum(u1 > 0 for *_, u1 in r)), H3_ゆっくり忘れている途中=int(sum(u1 < u0 for *_, u0, u1 in r)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = dict(P養_切らない=round(float(np.median([x[1] for x in r])), 3), P養_切る=round(float(np.median([x[2] for x in r])), 3), u養_7000=round(float(np.median([x[3] for x in r])), 4), u養_15000=round(float(np.median([x[4] for x in r])), 4))
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
