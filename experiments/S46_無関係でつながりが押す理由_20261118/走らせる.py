import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
import 走らせる as B   # S30：換算型（c=30）と S16 世界（感覚256・雑音0.3）
W = B.W
記録 = {}
class 記す(B.換算):
    """選ぶ時の u・v食・ê の (一番の手 − 他の手の平均) を記録するだけ"""
    一番 = 0
    def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; 記録[i] = []
    def 選ぶ(s, φ):
        u = s.つながり.予測(φ); ê = np.array([m.予測(φ) for m in s.評価]); b = 記す.一番
        記録[s.番].append((u, s.v食, ê[b] - np.mean(np.delete(ê, b)))); return super().選ぶ(φ)
def 一番を調べる(s):
    世 = np.random.default_rng([s, 0]); 好み = np.array(W.養育者の好み)[世.permutation(W.行動数)]; return int(np.argmax(好み))
def 一生(s, 記録する=True, 寿命=8000):
    W.我慢の代価 = 0.0; W.学び率 = 0.01; B.v時定数 = 5000.0; 記録.clear(); 記す.一番 = 一番を調べる(s)
    W.赤ちゃん = 記す if 記録する else B.換算
    try: return W.一生(s, '無関係', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ')
    finally: W.我慢の代価 = 0.01; W.学び率 = 0.05; B.v時定数 = 1000.0; W.赤ちゃん = B.原
def one(s):
    o = 一生(s); assert o['一番'] == 記す.一番
    R = np.array([記録[i] for i in range(8)]).transpose(1, 0, 2); 相 = o['相手列']
    def 窓(a, b):
        m = 相[a:b] == 0; return [[float(R[a:b][m][:, k].mean()), float(R[a:b][~m][:, k].mean())] for k in range(3)]
    return dict(種=s, 初め=窓(0, 500), 育=窓(7000, 8000), 見られ分け育=float(np.mean([B.区(o, 7000, 7500)[2], B.区(o, 7500, 8000)[2]])))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        a = 一生(12699, False, 600); b = 一生(12699, True, 600); print('記録しても一生は同じ:', a['sha256'] == b['sha256'], ' 一番一致:', b['一番'] == 記す.一番); sys.exit()
    段 = sys.argv[1]; S = range(12600, 12630) if 段 == '本' else range(12700, 12730)
    with Pool(8) as p: rows = p.map(one, list(S))
    res = dict(H1_u養が正=int(sum(r['育'][0][0] > 0 for r in rows)), H2_u養が他より大=int(sum(r['育'][0][0] > r['育'][0][1] for r in rows)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    名 = ['u', 'v食', 'ê差']
    res['中央値'] = {w: {名[k]: [round(float(np.median([r[w][k][j] for r in rows])), 4) for j in range(2)] for k in range(3)} for w in ['初め', '育']}
    res['見られ分け育_中央値'] = round(float(np.median([r['見られ分け育'] for r in rows])), 3)
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=rows), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
