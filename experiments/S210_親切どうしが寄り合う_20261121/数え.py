"""S208：S205 の世界・頭をそのまま読み、β0（寄らない＝親切が損）・寿命16000・選び替え 2000手から250手ごと。終わりの親切な子の数（最後の8回＝2000手ぶんの平均、はじめ4）。"""
import importlib.util, numpy as np
_sp = importlib.util.spec_from_file_location('S210共', '../S210_親切どうしが寄り合う_20261121/共.py'); C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C)
def 測る(s, kG=1.0, β=0.0, 選=(2000, 250), 寿命=16000, 親切=3.0, δ=0.0):
    o = C.一生(s, 'v4', 寿命, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=kG, 寄る=β, 困寄る=0.0, 親切=親切, 親切組=(0, 1, 2, 3), 選び替え=選, 同類=δ)
    if 寿命 < 16000: return o['sha256']
    x = o['親切数列']; return float(np.mean(x[-8:])), float(np.mean(x[len(x) // 2 - 4:len(x) // 2 + 4])), o['sha256']
