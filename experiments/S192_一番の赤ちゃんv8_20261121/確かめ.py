"""(1) 7つの章の世界で v8＝v4（各3種・8000手）、対照 v4≠元。(2) なぐさめの世界（S189・泣き1%）で v8＝S189 の kE50（見本が無いので代理は働かない）。(3) 見て学ぶ世界（S168）で v8＝v7（共感量が無いので共感は働かない）。どれも別の処理で。"""
import sys, importlib.util
from multiprocessing import Pool
P = '../'
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
def 並(job):
    w, 名, s = job; G = L('S192一覧', P + 'S192_一番の赤ちゃんv8_20261121/一覧.py'); return G.並び((w, G.構成[名], s))
def なぐさめ世界(x):
    if x == '旧':
        sys.path.insert(0, P + 'S189_泣いている子_20261121'); import 共; return 共.一生(900, 'v4', 3000, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01)['sha256']
    sys.path.insert(0, P + 'S189_泣いている子_20261121'); import 共; V = L('S192v2', P + 'S192_一番の赤ちゃんv8_20261121/v2.py')
    共.V = V; 共.包 = V.に(共.B.換算, 共.W, 共.B); 共.構成['v8'] = dict(共.構成['v4'], k代理=3.0); return 共.一生(900, 'v8', 3000, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01)['sha256']
def 見本世界(x):
    sys.path.insert(0, P + 'S168_見て学ぶ_20261120'); import 共
    if x == '新':
        V = L('S192v2', P + 'S192_一番の赤ちゃんv8_20261121/v2.py'); 共.V = V; 共.包 = V.に(共.B.換算, 共.W, 共.B); 共.構成['v4'] = dict(共.構成['v4'], kE=50.0)
    return 共.一生(900, '見る', 'v4', 3000, 種類=(1500,), k代理=3.0)['sha256']
if __name__ == '__main__':
    W = ['48', '64', '116', '122', '125', '150', '164']; S = [900, 901, 902]; jobs = [(w, 名, s) for 名 in ['v4', 'v8', '元'] for w in W for s in S]
    with Pool(8, maxtasksperchild=1) as p:
        r = dict(zip(jobs, p.map(並, jobs, chunksize=1))); a = p.map(なぐさめ世界, ['旧', '新'], chunksize=1); b = p.map(見本世界, ['旧', '新'], chunksize=1)
    print('7世界 v8＝v4:', sum(r[(w, 'v4', s)] == r[(w, 'v8', s)] for w in W for s in S), '/21  対照 v4≠元:', sum(r[(w, 'v4', s)] != r[(w, '元', s)] for w in W for s in S), '/21')
    print('なぐさめの世界 v8＝S189 kE50:', a[0] == a[1], ' 見て学ぶ世界 v8＝v7:', b[0] == b[1])
