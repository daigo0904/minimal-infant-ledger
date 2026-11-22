"""S227：頭は S226 と同じ v4（S30 の換算型＋v2・kf3・kD30・λ0.2・kJ5・J満・損も）＋共感 kE。世界は S227 の言葉が要る世界。"""
import numpy as np, importlib.util, sys
P = '../'
sys.path.insert(0, P + 'S30_換算型その手だけ_20261118')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
B = L('S228B', P + 'S30_換算型その手だけ_20261118/走らせる.py'); W = B.W
N = L('S228世界', P + 'S228_二人だけの言葉_20261121/世界.py')
V = L('S228v2', P + 'S228_二人だけの言葉_20261121/v2.py'); 包 = V.に(B.換算, W, B)
構成 = {'v4': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満', 損も=True)}
def 一生(s, 寿命=16000, kE=50.0, 見える=False, 組み方='毎回'):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False, kE=kE); V.設定.update(構成['v4'])
    W.学び率 = 0.01; B.v時定数 = 5000.0
    try: return N.一生(s, 包, W, 寿命=寿命, 見える=見える, 組み方=組み方)
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0; W.見た目次元 = 8
