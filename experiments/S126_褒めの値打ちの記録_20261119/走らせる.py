"""S125 の作り（褒める・一番の赤ちゃん・手8）で、養育者が見ている手ごとに u・ê・q・v食 を記録。初め（0〜1000）と終わり（7000〜8000）で、
つながりの項 c·v食·u·ê の 指す手 − 取る手 の差、Q の 指す手 − 取る手 の差、u・ê[指す]・v食 を比べる。"""
import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S125叙頭', '../S125_叙述的指さし_20261119/叙頭.py')
記 = {}
def 記録つき(基):
    class K(基):
        def __init__(s, 種, i, 頭): super().__init__(種, i, 頭); s.番 = i; s.t = 0; 記[i] = dict(u=np.zeros(8000), v=np.zeros(8000), ê=np.zeros((8000, 8)), q=np.zeros((8000, 8)))
        def 選ぶ(s, φ):
            a, q, ê = super().選ぶ(φ)
            if s.t < 8000: R = 記[s.番]; R['u'][s.t] = s.つながり.予測(φ); R['v'][s.t] = max(s.v食, 0.0); R['ê'][s.t] = ê; R['q'][s.t] = q
            s.t += 1; return a, q, ê
    return K
H.食換算 = 記録つき(H.A2.換算に(H.原換算, H.W, H.B))
def one(s):
    記.clear(); o = H.一生(s, '褒める'); 相 = o['相手列']; out = []
    for lo, hi in [(0, 1000), (7000, 8000)]:
        v = []
        for i in range(8):
            m = np.arange(lo, hi)[相[lo:hi, i] == 0]; R = 記[i]; 項 = H.B.c * R['v'][m, None] * R['u'][m, None] * R['ê'][m]
            v.append([float((項[:, 4:].mean(1) - 項[:, :4].mean(1)).mean()), float((R['q'][m, 4:].mean(1) - R['q'][m, :4].mean(1)).mean()), float(R['u'][m].mean()), float(R['ê'][m, 4:].mean()), float(R['v'][m].mean())])
        out += list(np.mean(v, 0))
    return [s] + out
名 = ['項の指す−取る', 'Qの指す−取る', 'u養育者', 'ê指す', 'v食']
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        s = 28799; 元 = L('S125叙頭元', '../S125_叙述的指さし_20261119/叙頭.py'); print('記録つきは手を加えていない S125 と同じ sha:', H.一生(s, '褒める', 寿命=1000)['sha256'] == 元.一生(s, '褒める', 寿命=1000)['sha256']); 記.clear(); r = one(s)
        print('初め:', dict(zip(名, np.round(r[1:6], 4))), '\n終わり:', dict(zip(名, np.round(r[6:11], 4)))); sys.exit()
    段 = sys.argv[1]; S = range(28600, 28630) if 段 == '本' else range(28700, 28730)
    with Pool(8) as p: r = p.map(one, list(S))
    res = {'H1_指す手のつながりの項の上乗せが下がる': int(sum(x[6] < x[1] for x in r)), 'H2_養育者へのつながり u が下がる': int(sum(x[8] < x[3] for x in r)), 'H3_癖（Q）が指す手を下げる': int(sum(x[7] < x[2] for x in r))}
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['中央値'] = {段_: {n: round(float(np.median([x[1 + 5 * j + k] for x in r])), 4) for k, n in enumerate(名)} for j, 段_ in enumerate(['初め', '終わり'])}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
