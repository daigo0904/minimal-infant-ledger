import sys, importlib.util
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S183_記憶のどこが効くか_20261120'); import 数え; return 数え.長く(900, 0.5, x, 寿命=1500)
def 旧(_):
    sp = importlib.util.spec_from_file_location('S182数え', '../S182_長く育てる_20261120/数え.py'); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    S = m.S; V, M = S.G.かける('122'); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False); V.設定.update(S.G.構成['v4']); M.A2.設定['kf'] = 0.0
    S.N2.視線隠す = True; S.N2.漂い = 'いない時'; S.N2.記憶 = 0.5; S.N2.記憶W = M.H.W; M.H.N = S.N2; return M.H.一生(900, 0.0, True, 寿命=1500)['sha256']
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a = p.map(新, ['両方', '顔だけ', '手だけ'], chunksize=1); b = p.map(旧, [0])[0]
    print('両方＝S182:', a[0] == b, ' 3つが互いに違う:', len(set(a)) == 3)
