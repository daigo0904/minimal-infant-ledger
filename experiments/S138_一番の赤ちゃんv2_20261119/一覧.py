"""調整用の種 900〜909：元／+食べ予測／+欠乏／+λ0.2／全部 で5つの章の主な数字。
世界ごとに別の処理で読み込む（S116 と S122 は同じ名前の部品「共通」を読むので、同じ処理で読むと先のものが使い回される）。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
P = '../'
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
構成 = {'元': dict(), '+食べ予測': dict(kf=3.0), '+欠乏': dict(kD=30.0), '+λ0.2': dict(λ=0.2), '全部': dict(kf=3.0, kD=30.0, λ=0.2)}
_m = {}
def 用意(世界):
    if 世界 in _m: return _m[世界]
    V = L('S138v2', P + 'S138_一番の赤ちゃんv2_20261119/v2.py')
    if 世界 == '48': M = L('S48R', P + 'S48_得と邪魔を分ける_20261118/走らせる.py'); Bm, Wm = M.S47.B, M.S47.W
    elif 世界 == '64': M = L('S64R', P + 'S64_構われないと_20261118/走らせる.py'); Bm, Wm = M.B, M.W
    elif 世界 == '116': M = L('S116頭', P + 'S116_視線は読めるか_20261119/頭.py'); Bm, Wm = M.B, M.W
    elif 世界 == '122': M = L('S123選び', P + 'S123_指す手柄_20261119/選び.py'); Bm, Wm = M.H.B, M.H.W
    else: M = L('S125叙頭', P + 'S125_叙述的指さし_20261119/叙頭.py'); Bm, Wm = M.B, M.W
    元 = Bm.換算; 包 = V.に(元, Wm, Bm); _m[世界] = (V, M, Bm, 包); return _m[世界]
def かける(世界):
    V, M, Bm, 包 = 用意(世界); Bm.換算 = 包
    if 世界 == '122': M.H.食換算 = 包
    if 世界 == '125': M.食換算 = 包
    if 世界 == '116': M.食べ予測 = 包
    return V, M
def one(job):
    s, 名, 世界 = job; V, M = かける(世界); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3); V.設定.update(構成[名])
    if 世界 == '48': o = M.一生(s, '本物'); return float(np.mean([M.S47.B.区(o, 7000, 7500)[2], M.S47.B.区(o, 7500, 8000)[2]]))
    if 世界 == '64': a = M.一生(s, '欠乏'); かける(世界); b = M.一生(s, 'なし'); return M.P養(a, 7500, 7700) - M.P養(b, 7500, 7700)
    if 世界 == '116': return M.持ち上がり(M.C.一生(s, 4, '本物', 学び率=0.01), 7000, 8000)[1]
    if 世界 == '122': M.A2.設定['kf'] = 0.0; return M.指す場面(M.H.一生(s, 0.0, True), 7000, 8000)[0]
    o = M.一生(s, '褒める'); return M.指す(o, 7000, 8000)[0] - M.指す(o, 0, 1000)[0]
def 並び(job):
    世界, cfg = job; V, M = かける(世界); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3); V.設定.update(cfg)
    f = {'48': lambda: M.一生(900, '本物', 1500), '64': lambda: M.一生(900, '欠乏', 1500), '116': lambda: M.C.一生(900, 4, '本物', 寿命=1500, 学び率=0.01), '122': lambda: M.H.一生(900, 0.0, True, 寿命=1500), '125': lambda: M.一生(900, '褒める', 寿命=1500)}[世界]
    return f()['sha256']
世界一覧 = ['48', '64', '116', '122', '125']
if __name__ == '__main__':
    if sys.argv[1:] == ['確かめ']:
        with Pool(5, maxtasksperchild=1) as p:
            a = p.map(並び, [(w, {}) for w in 世界一覧]); b = p.map(並び, [(w, dict(kf=3.0, kD=30.0, λ=0.2)) for w in 世界一覧])
        print('全部で手が変わる:', dict(zip(世界一覧, [x != y for x, y in zip(a, b)])))
        with Pool(5, maxtasksperchild=1) as p: c = p.map(並び, [(w, 'x') for w in []])
        sys.exit()
    with Pool(8, maxtasksperchild=1) as p:
        r = p.map(one, [(s, 名, w) for 名 in 構成 for w in 世界一覧 for s in range(900, 910)], chunksize=1)
    import json; json.dump(dict(構成=list(構成), 世界=世界一覧, 値=[float(x) for x in r]), open('一覧.json', 'w'), ensure_ascii=False)
    r = np.array(r).reshape(len(構成), len(世界一覧), 10)
    for k, 名 in enumerate(構成):
        m = np.median(r[k], 1)
        print(f'{名}: S48 見られ分け {m[0]:.3f} | S64 甘えの増え {m[1]:+.3f}（>0 {int((r[k,1]>0).sum())}/10） | S116 真ん中の視線追い {m[2]:+.3f} | S123 当たりを指す {m[3]:.3f} | S127 指すの育ち {m[4]:+.3f}（>0 {int((r[k,4]>0).sum())}/10）')
