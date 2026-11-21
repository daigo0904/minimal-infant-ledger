"""S222：S221 の数え方（見た分だけ・噂0.05・並びの信用・選び替えなし・親切4・親切でない4・席を入れ替えた2一生・β0・ρ5）。
嘘つき＝親切でない側の1人（子7／子3）、標的＝親切側の端（子0／子7）。悪口なしは嘘つきを置かない（標的の席は同じに数える）。
標的の損＝後半8000手の 標的の空腹 − 他の親切な子3人の空腹。嘘つきへの信用・正直への信用（嘘つき以外の子が持つ値）。標的の評判＝標的以外・嘘つき以外が持つ 私評[・, 標的] の平均 − 他の親切な子の評判の平均。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S222共', '../S222_狙い撃ちの悪口_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, 親切組, 嘘つき=None, 悪口=None, 信用='並び', 寿命=16000, 噂=0.05):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=親切組, 選び替え=None, 同類=0.0, 評判=5.0, 私的='見た', 噂=噂, 嘘つき=嘘つき, 信用=信用, 悪口=悪口)
def 測る(s, 悪=True, 寿命=16000):
    r = []
    for 親, 嘘番, 標 in [((0, 1, 2, 3), 7, 0), ((4, 5, 6, 7), 3, 7)]:
        o = 一生(s, 親, 嘘番 if 悪 else None, 標 if 悪 else None, 寿命=寿命); H = o['h列'][len(o['h列']) // 2:]; 他 = [k for k in 親 if k != 標]
        P, 信 = o['私評'], o['信']; 見手 = [i for i in range(8) if i not in (嘘番, 標)]
        評差 = np.mean([P[i, 標] for i in 見手]) - np.mean([P[i, k] for i in 見手 for k in 他 if k != i])
        r.append((H[:, 標].mean() - H[:, 他].mean(), float(np.mean([信[i, 嘘番] for i in range(8) if i != 嘘番])), float(np.mean([信[i, j] for i in range(8) if i != 嘘番 for j in range(8) if j not in (i, 嘘番)])), float(評差), o['sha256']))
    return [float(np.mean([x[k] for x in r])) for k in range(4)] + [r[0][4]]
