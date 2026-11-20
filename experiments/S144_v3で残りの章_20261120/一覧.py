"""調整用の種 900〜909：元／v3 で S135 順番交代（交代の世界の差 7000〜8000）と S90 信頼の入れ替わり（入れ替え後に新しいお手本＝番号2 を写す割合 − 古いお手本＝番号1）。世界ごとに別の処理。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
P = '../'
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
構成 = {'元': dict(), 'v3': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満')}
_m = {}
def 用意(世界):
    if 世界 in _m: return _m[世界]
    V = L('S142v2', P + 'S142_空腹で切り替える_20261120/v2.py')
    if 世界 == '135': M = L('S135共', P + 'S135_順番交代_20261119/共.py'); Bm, Wm = M.B, M.W
    else: M = L('S90R', P + 'S90_信頼の入れ替わり_20261119/走らせる.py'); Bm, Wm = M.B, M.W
    _m[世界] = (V, M, Bm, V.に(Bm.換算, Wm, Bm)); return _m[世界]
def かける(世界):
    V, M, Bm, 包 = 用意(世界); Bm.換算 = 包; return V, M
def 設定(V, cfg): V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None); V.設定.update(cfg)
def one(job):
    s, 名, 世界 = job; V, M = かける(世界); 設定(V, 構成[名])
    if 世界 == '135':
        a = M.数える(M.一生(s, '交代'), 7000, 8000)[2]; かける(世界); b = M.数える(M.一生(s, 'でたらめ'), 7000, 8000)[2]; return [a, b]
    o = M.一生(s, True); x = M.数(o, 7000, 8000); y = M.数(o, 3000, 4000); return [x[1] - x[0], y[0] - y[1]]
def 並び(job):
    世界, cfg = job; V, M = かける(世界); 設定(V, cfg)
    return (M.一生(900, '交代', 1500) if 世界 == '135' else M.一生(900, True, 1500))['sha256']
def 元並び(世界):
    _, M, Bm, _ = 用意(世界); return (M.一生(900, '交代', 1500) if 世界 == '135' else M.一生(900, True, 1500))['sha256']
世界一覧 = ['135', '90']
if __name__ == '__main__':
    if sys.argv[1:] == ['確かめ']:
        with Pool(2, maxtasksperchild=1) as p:
            a = p.map(元並び, 世界一覧, chunksize=1); b = p.map(並び, [(w, {}) for w in 世界一覧], chunksize=1); c = p.map(並び, [(w, 構成['v3']) for w in 世界一覧], chunksize=1)
        print('v3（全部0）は元と同じ:', dict(zip(世界一覧, [x == y for x, y in zip(a, b)])), ' v3 で手が変わる:', dict(zip(世界一覧, [x != y for x, y in zip(b, c)]))); sys.exit()
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, [(s, 名, w) for 名 in 構成 for w in 世界一覧 for s in range(900, 910)], chunksize=1)
    r = np.array(r).reshape(len(構成), len(世界一覧), 10, 2)
    for k, 名 in enumerate(構成):
        m135 = np.median(r[k, 0], 0); m90 = np.median(r[k, 1], 0)
        print(f'{名}: S135 交代の差 {m135[0]:+.3f}（でたらめ {m135[1]:+.3f}、交代>でたらめ {int((r[k,0,:,0] > r[k,0,:,1]).sum())}/10） | S90 入れ替え後 新しいお手本−古い {m90[0]:+.3f}（>0 {int((r[k,1,:,0] > 0).sum())}/10）・入れ替え前 お手本−でたらめ {m90[1]:+.3f}')
