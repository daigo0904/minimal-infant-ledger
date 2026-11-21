"""S223：S222 の数え方（見た分だけ・並びの信用・選び替えなし・親切4・親切でない4・席を入れ替えた2一生・β0・ρ5・嘘つき 子7／子3・標的 子0／子7）。
標的の損・嘘つきへの信用・標的の評判差（S222 と同じ）に加え、表の相関（嘘つき以外の子の 終わりの表 と 本当のなぐさめ割合（最後の2000手）の相関の平均）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S223共', '../S223_自分の目を信じる_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, 親切組, 嘘つき=None, 悪口=None, 信用='並び', 寿命=16000, 噂=0.05, ふるい=None):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=親切組, 選び替え=None, 同類=0.0, 評判=5.0, 私的='見た', 噂=噂, 嘘つき=嘘つき, 信用=信用, 悪口=悪口, ふるい=ふるい)
def 測る(s, 悪=True, ふるい=None, 噂=0.05, 寿命=16000):
    r = []
    for 親, 嘘番, 標 in [((0, 1, 2, 3), 7, 0), ((4, 5, 6, 7), 3, 7)]:
        o = 一生(s, 親, 嘘番 if 悪 else None, 標 if 悪 else None, 寿命=寿命, 噂=噂, ふるい=ふるい); H = o['h列'][len(o['h列']) // 2:]; 他 = [k for k in 親 if k != 標]
        P, 信 = o['私評'], o['信']; 見手 = [i for i in range(8) if i not in (嘘番, 標)]
        評差 = np.mean([P[i, 標] for i in 見手]) - np.mean([P[i, k] for i in 見手 for k in 他 if k != i])
        真 = (o['行動列'][-2000:] == 3).mean(0); c = []
        for i in range(8):
            if i == 嘘番: continue
            m = np.arange(8) != i
            if P[i, m].std() > 0 and 真[m].std() > 0: c.append(np.corrcoef(P[i, m], 真[m])[0, 1])
        r.append((H[:, 標].mean() - H[:, 他].mean(), float(np.mean([信[i, 嘘番] for i in range(8) if i != 嘘番])), float(評差), float(np.mean(c)) if c else np.nan, o['sha256']))
    return [float(np.nanmean([x[k] for x in r])) for k in range(4)] + [r[0][4]]
