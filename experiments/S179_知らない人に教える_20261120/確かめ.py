import sys
from multiprocessing import Pool
def 新(名):
    sys.path.insert(0, '../S179_知らない人に教える_20261120'); import 数え; return 数え.測る(900, 名)[-1]
def 旧(名):
    import importlib.util; sp = importlib.util.spec_from_file_location('S152一覧', '../S152_一番の赤ちゃんv4_20261120/一覧.py'); G = importlib.util.module_from_spec(sp); sp.loader.exec_module(G)
    V, M = G.かける('122'); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False); V.設定.update(G.構成[名]); M.A2.設定['kf'] = 0.0
    return M.H.一生(900, 0.0, True)['sha256']
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a = p.map(新, ['元', 'v4'], chunksize=1); b = p.map(旧, ['元', 'v4'], chunksize=1)
    print('数え.py の一生＝S152 の作り（元・v4）:', a == b, ' 元≠v4:', a[0] != a[1])
