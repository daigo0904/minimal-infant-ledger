import sys, numpy as np
import importlib.util
sys.path.insert(0, '../S30_換算型その手だけ_20261118')
sp = importlib.util.spec_from_file_location('S45', '../S45_代価0で効きの対照_20261118/走らせる.py'); S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
B = S.B; W = S.W
違う = []
class 数える(S.切れる):
    def 選ぶ(s, φ):
        q = s.Q @ φ; ê = np.array([m.予測(φ) for m in s.評価]); u = s.つながり.予測(φ)
        sc = q + B.c * max(s.v食, 0.0) * u * ê
        if s.手数 >= 7000: 違う.append(int(np.argmax(sc) != np.argmax(q)))
        return super().選ぶ(φ)
S.切れる.__init__  # noop
W.我慢の代価 = 0.0; W.学び率 = 0.01; B.v時定数 = 5000.0; W.赤ちゃん = 数える; S.窓[0] = None
o = W.一生(12600, '無関係', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='その手だけ')
print('7000〜で link ありと Q だけの argmax が違う割合:', np.mean(違う), ' 見られ分け:', B.区(o, 7000, 8000)[2])
