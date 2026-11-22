"""調整用の種 900〜909：λ=1/0.5/0.2 で S125（叙述的指さし・褒める）・S64（構われないと）・S48（本物の見られ分け）。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
G = L('S127重み', '../S127_癖の重み_20261119/重み.py')
H125 = L('S125叙頭', '../S125_叙述的指さし_20261119/叙頭.py'); H125.食換算 = G.に(H125.原換算, H125.W, H125.B)
R64 = L('S64R', '../S64_構われないと_20261118/走らせる.py')
R48 = L('S48R', '../S48_得と邪魔を分ける_20261118/走らせる.py')
# 全部読み込んでから差し替える（後から読んだものが前の差し替えを戻していた）。同じ型を二重に包まない
for _B, _W in [(R64.B, R64.W), (R48.S47.B, R48.S47.W)]:
    if not getattr(_B.換算, '_λ', False): _B.換算 = G.に(_B.換算, _W, _B); _B.換算._λ = True
包 = {id(_B): _B.換算 for _B in [R64.B, R48.S47.B]}   # S125 の頭が一生の後に共有の 換算 を元へ戻すので、毎回かけ直す
def かけ直す():
    for _B in [R64.B, R48.S47.B]: _B.換算 = 包[id(_B)]
def one(job):
    s, λ = job; G.設定['λ'] = λ
    try:
        o = H125.一生(s, '褒める'); p0, _, _ = H125.指す(o, 0, 1000); p1, _, f1 = H125.指す(o, 7000, 8000)
        o2 = H125.一生(s, '褒めない'); q1 = H125.指す(o2, 7000, 8000)[0]
        かけ直す(); assert getattr(R64.B.換算, '_λ', False) and getattr(R48.S47.B.換算, '_λ', False)
        a = R64.一生(s, '欠乏'); b = R64.一生(s, 'なし'); 増 = R64.P養(a, 7500, 7700) - R64.P養(b, 7500, 7700)
        o3 = R48.一生(s, '本物'); 見 = float(np.mean([R48.S47.B.区(o3, 7000, 7500)[2], R48.S47.B.区(o3, 7500, 8000)[2]]))
    finally: G.設定['λ'] = 1.0
    return [p0, p1, q1, f1, 増, R64.P養(b, 7500, 7700), 見]
if __name__ == '__main__':
    with Pool(8) as p:
        for λ in [1.0, 0.5, 0.2]:
            r = np.array(p.map(one, [(s, λ) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'λ={λ}: S125 指す 褒める 初め {m[0]:.3f}→終わり {m[1]:.3f}（育つ {int((r[:,1] > r[:,0]).sum())}/10）・褒めない {m[2]:.3f} 食べ {m[3]:.4f} | S64 増え {m[4]:+.3f}（>0 {int((r[:,4] > 0).sum())}/10）P養 {m[5]:.3f} | S48 本物 {m[6]:.3f}')
