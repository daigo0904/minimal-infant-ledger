"""S236：S235 の写し。聞き方＝'分けて'：聞き手は 行を選ぶ時は1つ目の合図だけ、列を選ぶ時は2つ目の合図だけを入力に入れる（耳で話す時の「自分が聞き手なら」も同じ）。
S235 組み合わせる言葉（文法の芽）：ご飯は 16 か所（行 r・列 c、各4）。
毎手 乱数［種,40］で 4組（話し手・聞き手）に組み替え、乱数［種,41］で各組の場所。未見＝(手数) まではその4か所（対角）を出さない。
話し手：1つ目の合図（入力＝行・列・印S1）、2つ目の合図（入力＝行・列・1つ目・印S2）。各 4つの手。
聞き手：入力＝1つ目・2つ目の合図・印。まず行を選び（印R）、次に列を選ぶ（印C）。両方当たれば食べる。
話し方＝'耳'：話し手は、自分が聞き手として (合図1, 合図2) を聞いたら 行 r の点＋列 c の点 が一番高い組を出す（乱数［種,42］で 0.1 はでたらめ）。
入力 20次元＝行4・列4・合図1 4・合図2 4・印4（S1,S2,R,C）。共感：聞き手が食べたら h² の減り分を話し手の共感量に。"""
import hashlib, numpy as np
人数 = 8; 次元 = 20; 未見組 = [(0, 0), (1, 1), (2, 2), (3, 3)]
def 入(r=None, c=None, t1=None, t2=None, 印=0):
    x = np.zeros(次元)
    if r is not None: x[r] = 1.0; x[4 + c] = 1.0
    if t1 is not None: x[8 + t1] = 1.0
    if t2 is not None: x[12 + t2] = 1.0
    x[16 + 印] = 1.0; return x
def 一生(種, 包, W, 寿命=16000, 話し方='ふつう', 点=None, 未見まで=None, 頭='獲得型', 聞き方='まとめて'):
    W.見た目次元 = 次元
    分 = 聞き方 == '分けて'   # S236
    行入 = lambda u, v: 入(t1=u, t2=None if 分 else v, 印=2); 列入 = lambda u, v: 入(t1=None if 分 else u, t2=v, 印=3)
    子 = [包(種, i, 頭) for i in range(人数)]
    組乱 = np.random.default_rng([種, 40]); 場乱 = np.random.default_rng([種, 41]); 耳乱 = np.random.default_rng([種, 42])
    見る場 = [(r, c) for r in range(4) for c in range(4) if (r, c) not in 未見組]
    列 = {k: np.zeros((寿命, 4), dtype=np.int8) for k in ['話', '聞', '行', '列', 'a1', 'a2', 'b1', 'b2']}; 当列 = np.zeros((寿命, 4), dtype=bool)
    h列 = np.zeros((寿命 // 100, 人数)); sha = hashlib.sha256()
    for t in range(寿命):
        並 = 組乱.permutation(人数); 隠 = 未見まで is not None and t < 未見まで
        for p in range(4):
            sp, li = int(並[2 * p]), int(並[2 * p + 1])
            if 隠: r, c = 見る場[int(場乱.integers(len(見る場)))]
            else: k = int(場乱.integers(16)); r, c = k // 4, k % 4
            S = 子[sp]; L = 子[li]
            φ1 = S.感覚(入(r, c, 印=0)); a1, q1, _ = S.選ぶ(φ1)
            if 話し方 == '耳':
                if 耳乱.random() < 0.1: a1 = int(耳乱.integers(4)); a2e = int(耳乱.integers(4))
                else:
                    best, a2e = -1e9, 0
                    for u in range(4):
                        for v in range(4):
                            sc = 点(S, S.感覚(行入(u, v)))[r] + 点(S, S.感覚(列入(u, v)))[c]
                            if sc > best: best, a1, a2e = sc, u, v
            φ2 = S.感覚(入(r, c, t1=a1, 印=1)); a2, q2, _ = S.選ぶ(φ2)
            if 話し方 == '耳': a2 = a2e
            φr = L.感覚(行入(a1, a2)); b1, qr, _ = L.選ぶ(φr)
            φc = L.感覚(列入(a1, a2)); b2, qc, _ = L.選ぶ(φc)
            当 = (b1 == r) and (b2 == c); 前h = L.h
            S.受ける(φ1, a1, q1, 0.0, False, 0.0); S.受ける(φ2, a2, q2, 0.0, False, 0.0)
            L.受ける(φr, b1, qr, 0.0, False, 0.0); L.受ける(φc, b2, qc, 0.0, bool(当), 0.0)
            S.共感量 = 前h ** 2 - L.h ** 2 if 当 else 0.0
            for k_, v_ in zip(['話', '聞', '行', '列', 'a1', 'a2', 'b1', 'b2'], [sp, li, r, c, a1, a2, b1, b2]): 列[k_][t, p] = v_
            当列[t, p] = 当
        if t % 100 == 0: h列[t // 100] = [c_.h for c_ in 子]
        sha.update(列['a1'][t].tobytes()); sha.update(列['a2'][t].tobytes()); sha.update(当列[t].tobytes())
    return dict(当列=当列, h列=h列, sha256=sha.hexdigest(), **列)
