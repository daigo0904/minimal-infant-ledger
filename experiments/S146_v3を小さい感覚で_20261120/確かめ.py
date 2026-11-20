import sys, importlib.util
from multiprocessing import Pool
_sp = importlib.util.spec_from_file_location('S146一覧', '../S146_v3を小さい感覚で_20261120/一覧.py'); G = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(G)
def 見る(w):
    V, M = G.かける(w); Ws, Ns = G.小さく(w, M); Bm = G.用意(w)[2]
    c = Bm.換算(900, 0, '獲得型'); return w, c.感覚.W.shape[0], Ns.見た目雑音, G.並び((w, {})) != G.並び((w, G.構成['v3']))
if __name__ == '__main__':
    with Pool(5, maxtasksperchild=1) as p: print(p.map(見る, G.世界一覧, chunksize=1))
