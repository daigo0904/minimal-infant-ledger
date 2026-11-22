"""S227：頭は S226 と同じ v4（S30 の換算型＋v2・kf3・kD30・λ0.2・kJ5・J満・損も）＋共感 kE。世界は S227 の言葉が要る世界。"""
import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S234B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S234世界', P + 'S234_評判で組む_20261121/世界.py')
V = L('S234v2', P + 'S234_評判で組む_20261121/v2.py'); 包 = V.に(B.換算, W, B)
構成 = {'v4': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)}
def 点(子, φ):
    """v4 の手の点（e=0 の世界なので ê・kD の項はほぼ 0 として省く）：λ·Q＋kf·(食べ予測−平均)"""
    S = V.設定; q = 子.Q @ φ; f = np.array([m.予測(φ) for m in 子.食]); return S['λ'] * q + S['kf'] * (f - f.mean())
def 一生(s, 寿命=16000, kE=50.0, 見える=False, 組み方='毎回', 話し方='ふつう', 転入=None, 群れ=None, 入れ替え=None, 耳組=(), 選び替え=None, 組評判=0.0):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False, kE=kE); V.設定.update(構成['v4'])
    W.学び率 = 0.01; B.v時定数 = 5000.0
    try: return N.一生(s, 包, W, 寿命=寿命, 見える=見える, 組み方=組み方, 話し方=話し方, 点=点, 転入=転入, 群れ=群れ, 入れ替え=入れ替え, 耳組=耳組, 選び替え=選び替え, 組評判=組評判)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
