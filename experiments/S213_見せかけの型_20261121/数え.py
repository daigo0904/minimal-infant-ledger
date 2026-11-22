"""S213：S212 の数え方（β0・ρ5・親切3・寿命16000・選び替え 2000手から250手ごと・kG1・観客入力）。はじめ 子0,1 いつも親切・子2,3 見せかけ。終わり（最後の8回の平均）の いつも親切の数・見せかけの数。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S213共', '../S213_見せかけの型_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, 見評=True, 見せ組=(2, 3), 寿命=16000, ρ=5.0, 観=True, 選=(2000, 250)):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=3.0, 親切組=(0, 1, 2, 3), 選び替え=選, 同類=0.0, 評判=ρ, 観客入力=観, 見られ評判=見評, 見せ組=見せ組)
    if 寿命 < 16000: return o['sha256']
    x, y = np.array(o['親切数列'], float), np.array(o['見せ数列'], float); 見 = float(np.mean(y[-8:])); return float(np.mean(x[-8:])) - 見, 見, o['sha256']
