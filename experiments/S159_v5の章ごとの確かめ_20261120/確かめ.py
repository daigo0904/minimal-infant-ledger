"""v5を1に（損重さ1）は、S152 の v4（5つの世界）・S151 の v3損も（情報探し）と同じ sha か。v5 は手が変わるか。どれも別の処理で読む。"""
import sys, importlib.util
from multiprocessing import Pool
P = '../'
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
def 新(job):
    w, 名 = job; G = L('S159一覧', P + 'S159_v5の章ごとの確かめ_20261120/一覧.py'); return G.並び((w, G.構成[名]))
def 旧(w):
    if w == '150':
        S = L('S151選び', P + 'S151_損も見る食べ予測_20261120/選び.py'); return S.C.一生(900, '見る', 'v3損も', 1500)['sha256']
    G = L('S152一覧', P + 'S152_一番の赤ちゃんv4_20261120/一覧.py'); return G.並び((w, G.構成['v4']))
if __name__ == '__main__':
    W = ['48', '64', '116', '122', '125', '150']
    with Pool(6, maxtasksperchild=1) as p:
        a = p.map(新, [(w, 'v5を1に') for w in W], chunksize=1); b = p.map(旧, W, chunksize=1); c = p.map(新, [(w, 'v5') for w in W], chunksize=1)
    print('損重さ1＝前の v4:', dict(zip(W, [x == y for x, y in zip(a, b)])))
    print('v5 で手が変わる:', dict(zip(W, [x != y for x, y in zip(a, c)])))
