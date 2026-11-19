import numpy as np, importlib.util
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
S = L('S129選び', '../S129_相手に効く欠乏_20261119/選び.py'); G, R = S.G, S.R
def 一生(s, 長さ, kD):
    """長さ>0 なら 7500−長さ 〜 7500 養育者が来ない（戻る時刻をそろえる）。長さ=0 は なし。"""
    G.設定.update(目安=0.05, 速=400.0, kD=kD); 原 = R.B.換算; R.B.換算 = S.包
    R.W.学び率 = 0.01; R.B.v時定数 = 5000.0; R.N.赤ちゃん = R.B.換算
    try: return R.N.一生(s, '依存', '獲得型', 寿命=8000, 離乳=8000, 給餌の形='その手だけ', 試し='欠乏' if 長さ else None, 試し始め=7500 - 長さ, 試し長さ=長さ)
    finally: R.B.換算 = 原; G.設定['kD'] = 0.0; R.W.学び率 = 0.05; R.B.v時定数 = 1000.0
def one(job):
    s, kD = job; b = R.P養(一生(s, 0, kD), 7500, 7700)
    return [R.P養(一生(s, L_, kD), 7500, 7700) - b for L_ in [250, 500, 1000]]
