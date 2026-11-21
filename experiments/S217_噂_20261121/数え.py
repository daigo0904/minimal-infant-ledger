"""S217：S216 の数え方（選び替えなし・親切4・親切でない4・席を入れ替えた2一生・β0・ρ5・後半8000手の空腹）。得＝親切でない−親切 の空腹差。
表の正しさ＝終わりの私評[i, 他] と 本当のなぐさめ割合（最後の2000手の手3の割合）の相関（i ごと→平均）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S217共', '../S217_噂_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, ρ, 私的, 親切組, 寿命=16000, 噂=0.0):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=親切組, 選び替え=None, 同類=0.0, 評判=ρ, 私的=私的, 噂=噂)
def 測る(s, ρ=5.0, 私的=False, 寿命=16000, 噂=0.0):
    r = []
    for 親 in [(0, 1, 2, 3), (4, 5, 6, 7)]:
        o = 一生(s, ρ, 私的, 親, 寿命, 噂); H = o['h列'][len(o['h列']) // 2:]; 不 = [i for i in range(8) if i not in 親]
        真 = (o['行動列'][-2000:] == 3).mean(0); P = o['私評']; c = []
        for i in range(8):
            m = np.arange(8) != i
            if P[i, m].std() > 0 and 真[m].std() > 0: c.append(np.corrcoef(P[i, m], 真[m])[0, 1])
        r.append((H[:, 不].mean() - H[:, list(親)].mean(), float(np.mean(c)) if c else np.nan, o['sha256']))
    return float(np.mean([x[0] for x in r])), float(np.nanmean([x[1] for x in r])), r[0][2]
