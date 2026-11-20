"""S182：S181 の数え.py（世界・頭）をそのまま読み、寿命を延ばして終わりの 2000手で数える。"""
import importlib.util
_sp = importlib.util.spec_from_file_location('S181数え', '../S181_記憶を足す_20261120/数え.py'); S = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(S)   # 同じ名前『数え』を避けてパスで読む
def 測る(s, α, 寿命=24000):
    V, M = S.G.かける('122'); V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None, 損も=False); V.設定.update(S.G.構成['v4']); M.A2.設定['kf'] = 0.0
    S.N2.視線隠す = True; S.N2.漂い = 'いない時'; S.N2.記憶 = α; S.N2.記憶W = M.H.W; M.H.N = S.N2
    o = M.H.一生(s, 0.0, True, 寿命=寿命); r = []
    for lo in [6000, 寿命 - 2000]:
        x = S.教える(o, lo, lo + 2000); r += [x[0] - x[1], x[2] - x[3], float(o['食列'][lo:lo + 2000].mean())]
    return tuple(r) + (o['sha256'],)   # 6000〜8000 の 指す差・取る差・食べ、終わり2000手の 指す差・取る差・食べ
