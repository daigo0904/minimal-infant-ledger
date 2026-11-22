"""調整用の種 900〜909：S141 世界（S125 と同じ＋共同注意の旗）で、v2 全部入り（kf3 kD30 λ0.2）と λ1 の頭に kJ=0/0.1/0.3/1。叙述的指さしの育ちと食べ。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
P = '../S141_共同注意の喜び_20261120/'
H = L('S141叙頭', P + '叙頭.py'); V = L('S141v2', P + 'v2.py'); 包 = V.に(H.原換算, H.W, H.B); H.食換算 = 包
def one(job):
    s, cfg = job; V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0); V.設定.update(cfg)
    o = H.一生(s, '褒める'); return [H.指す(o, 7000, 8000)[0] - H.指す(o, 0, 1000)[0], H.指す(o, 7000, 8000)[0], float(o['食列'][7000:].mean())]
構成 = {'全部 kJ3': dict(kf=3.0, kD=30.0, λ=0.2, kJ=3.0), '全部 kJ10': dict(kf=3.0, kD=30.0, λ=0.2, kJ=10.0), '食べ予測+欠乏 λ1 kJ0.3': dict(kf=3.0, kD=30.0, kJ=0.3), '食べ予測+欠乏 λ1 kJ1': dict(kf=3.0, kD=30.0, kJ=1.0)}
if __name__ == '__main__':
    if sys.argv[1:] == ['確かめ']:
        元 = L('S125元', '../S125_叙述的指さし_20261119/叙頭.py')
        V.設定.update(kJ=0.0); print('kJ0・元は S125 と同じ sha:', H.一生(28599, '褒める', 寿命=1500)['sha256'] == 元.一生(28599, '褒める', 寿命=1500)['sha256'])
        V.設定.update(kJ=1.0); print('kJ1 で手が変わる:', H.一生(28599, '褒める', 寿命=1500)['sha256'] != 元.一生(28599, '褒める', 寿命=1500)['sha256']); sys.exit()
    with Pool(8) as p:
        for 名, cfg in 構成.items():
            r = np.array(p.map(one, [(s, cfg) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'{名}: 叙述的指さしの育ち {m[0]:+.3f}（>0 {int((r[:,0] > 0).sum())}/10） 終わりの指す {m[1]:.3f} 食べ {m[2]:.4f}')
