"""S220：S219 の数え方（見た分だけ・噂0.05・選び替えなし・親切4・親切でない4・席を入れ替えた2一生・β0・ρ5・嘘つき＝親切でない側の1人）。
得・表の相関（嘘つき以外）に加え、嘘つき以外の子が持つ 嘘つきへの信用 と 正直な子（嘘つき・自分以外）への信用 の平均。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S221共', '../S221_並び方で見抜く_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, ρ, 私的, 親切組, 寿命=16000, 噂=0.0, 嘘つき=None, 信用=False):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=親切組, 選び替え=None, 同類=0.0, 評判=ρ, 私的=私的, 噂=噂, 嘘つき=嘘つき, 信用=信用)
def 測る(s, 嘘=True, 信用=False, 噂=0.05, 寿命=16000):
    r = []
    for 親, 嘘番 in [((0, 1, 2, 3), 7), ((4, 5, 6, 7), 3)]:
        o = 一生(s, 5.0, '見た', 親, 寿命, 噂, 嘘番 if 嘘 else None, 信用); H = o['h列'][len(o['h列']) // 2:]; 不 = [i for i in range(8) if i not in 親]
        真 = (o['行動列'][-2000:] == 3).mean(0); P, 信 = o['私評'], o['信']; c, 嘘信, 正信 = [], [], []
        for i in range(8):
            if i == 嘘番: continue
            m = np.arange(8) != i
            if P[i, m].std() > 0 and 真[m].std() > 0: c.append(np.corrcoef(P[i, m], 真[m])[0, 1])
            嘘信.append(信[i, 嘘番]); 正信 += [信[i, j] for j in range(8) if j not in (i, 嘘番)]
        r.append((H[:, 不].mean() - H[:, list(親)].mean(), float(np.mean(c)) if c else np.nan, float(np.mean(嘘信)), float(np.mean(正信)), o['sha256']))
    return [float(np.nanmean([x[k] for x in r])) for k in range(4)] + [r[0][4]]
