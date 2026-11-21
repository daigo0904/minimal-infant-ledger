"""S224：悪口なし・見た分だけ・並びの信用・選び替えなし・親切4・親切でない4・席を入れ替えた2一生・β0・ρ5。t=8000 に 親切でない側の端の子（子7／子3）が親切になる。
変わる子の評判 r_c(t)＝他の子の表の平均、親切な子の評判 r_k(t)＝親切な子どうしを除いた他の子の表の平均（100手ごと）。
追いつく手数＝8000以降で r_c ≥ r_c(8000) + 0.5·(r_k(t) − r_c(8000)) に初めてなるまで（届かなければ 8000）。空腹＝8000〜12000 の変わる子の空腹。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S224共', '../S224_頑固さの代価_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 一生(s, 親切組, 噂=0.05, ふるい=None, 変身=None, 寿命=16000):
    return C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=親切組, 選び替え=None, 同類=0.0, 評判=5.0, 私的='見た', 噂=噂, 嘘つき=None, 信用='並び', 悪口=None, ふるい=ふるい, 変身=変身)
def 測る(s, 噂=0.05, ふるい=None, 寿命=16000, 変わり目=8000):
    r = []
    for 親, 変 in [((0, 1, 2, 3), 7), ((4, 5, 6, 7), 3)]:
        o = 一生(s, 親, 噂, ふるい, (変わり目, 変), 寿命); E = o['評列']; b = 変わり目 // 100
        rc = np.array([np.mean([P[i, 変] for i in range(8) if i != 変]) for P in E])
        rk = np.array([np.mean([P[i, k] for k in 親 for i in range(8) if i != k]) for P in E])
        線 = rc[b] + 0.5 * (rk - rc[b]); 届 = np.where(rc[b:] >= 線[b:])[0]; 届 = [x for x in 届 if x > 0]
        手 = (届[0] * 100) if 届 else (寿命 - 変わり目)
        h = o['h列'][b:b + 40, 変].mean()
        r.append((手, h, rc[-1] - rc[b], o['sha256']))
    return float(np.mean([x[0] for x in r])), float(np.mean([x[1] for x in r])), float(np.mean([x[2] for x in r])), r[0][3]
