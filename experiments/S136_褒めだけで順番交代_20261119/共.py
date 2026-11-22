import numpy as np, importlib.util, sys
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S136B', '../S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S136世界', '../S136_褒めだけで順番交代_20261119/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
def 一生(s, 番, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.行動数 = 5; W.行動数 = 5; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9, -0.5]; W.見た目次元 = 9; N.赤ちゃん = B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 番=番)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; N.行動数 = 4; W.行動数 = 4; N.養育者の好み = [-0.8, -0.2, 0.3, 0.9]; W.見た目次元 = 8
def 数える(o, lo, hi):
    A, 相, 話 = o['行動列'][lo:hi], o['相手列'][lo:hi], o['話列'][lo:hi]; 養 = 相 == 0
    聞 = 養 & (話 == 0); 話中 = 養 & (話 == 1)
    return float((A[聞] < 4).mean()), float((A[話中] < 4).mean()), float((A[聞] < 4).mean() - (A[話中] < 4).mean()), float(o['食列'][lo:hi].mean())
