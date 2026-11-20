import sys, importlib.util
from multiprocessing import Pool
P = '../'
def 新(x):
    sys.path.insert(0, P + 'S175_相手ごとの好み_20261120'); import 共; o = 共.一生(900, 'v4', 1500, 二人=x); return o['sha256'], (float((o['相手列'] == 9).mean()), float((o['相手列'] == 0).mean()))
def 旧(_):
    sp = importlib.util.spec_from_file_location('S152一覧', P + 'S152_一番の赤ちゃんv4_20261120/一覧.py'); G = importlib.util.module_from_spec(sp); sp.loader.exec_module(G); return G.並び(('48', G.構成['v4']))
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: (a, _), (b, w) = p.map(新, [None, 0.5], chunksize=1); c = p.map(旧, [0])[0]
    print('二人なし＝S152 の 48・v4:', a == c, a[:8], c[:8], ' 二人で変わる:', a != b, ' B の割合・A の割合:', w)
