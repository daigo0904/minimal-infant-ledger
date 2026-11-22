"""種類なしの v4 は S151 の v3損も と同じ sha か。2つは別の処理で読む（どちらも『共』という名前の部品を読むので同じ処理だと先のものが使い回される）。"""
import sys, importlib.util
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S168_見て学ぶ_20261120'); import 共
    if x == 'なし': return 共.一生(900, '見る', 'v4', 1500)['sha256']
    if x == '種類': return 共.一生(900, '見る', 'v4', 1500, 種類=(700,))['sha256']
    return 共.一生(900, '見る', 'v4', 1500, 種類=(700,), k代理=1.0)['sha256']
def 旧(_):
    S = importlib.util.spec_from_file_location('S151選び', '../S151_損も見る食べ予測_20261120/選び.py'); G = importlib.util.module_from_spec(S); S.loader.exec_module(G)
    return G.C.一生(900, '見る', 'v3損も', 1500)['sha256']
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a, b, c = p.map(新, ['なし', '種類', '代理'], chunksize=1); d = p.map(旧, [0])[0]
    print('種類なし＝S151 v3損も:', a == d, a[:8], d[:8], ' 種類で変わる:', a != b, ' 代理で変わる:', b != c)
