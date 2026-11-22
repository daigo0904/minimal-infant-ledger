"""S215：選び替えなし・型固定（親切4・親切でない4）・β0・親切3・kG1・寿命16000。後半8000手の空腹（h列）。親切でない−親切 の空腹差（正＝親切が得）。席の違いを消すため、親切を子0〜3 にした一生と 子4〜7 にした一生の平均。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S215共', '../S215_私的な評判_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, ρ, 私的, 親切組, 寿命=16000):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=親切組, 選び替え=None, 同類=0.0, 評判=ρ, 私的=私的)
def 測る(s, ρ=5.0, 私的=False, 寿命=16000):
    r = []
    for 親 in [(0, 1, 2, 3), (4, 5, 6, 7)]:
        o = 一生(s, ρ, 私的, 親, 寿命); H = o['h列'][len(o['h列']) // 2:]; 不 = [i for i in range(8) if i not in 親]
        r.append((H[:, 不].mean() - H[:, list(親)].mean(), H[:, list(親)].mean(), H[:, 不].mean(), o['sha256']))
    return float(np.mean([x[0] for x in r])), float(np.mean([x[1] for x in r])), float(np.mean([x[2] for x in r])), r[0][3]
