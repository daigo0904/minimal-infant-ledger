"""S233：S232 の写し。話し方＝'型'：子ごとの印 耳（True なら耳で話す）。耳組＝はじめ耳の子。選び替え＝(始め, 間隔)：S205 と同じく 間隔ごとに 直近で一番お腹を空かせた子を新しい頭（種＋2000003＋n）に、印は一番お腹の空いていない子から受け継ぐ。耳数列＝間隔ごとの耳の子の数。
S232：S231 の写し。入れ替え＝(始め, 間隔)：始めから間隔ごとに、一番古い子（同じなら番号の小さい子）を生まれたての頭（種＋3000003＋n）に入れ替える。
S231：S230 の写し。群れ m（None なら無し）：子0〜3 と子4〜7。毎手、乱数［種,43］で 確率 m なら組乱の組（またぐ）、そうでなければ群れの中だけで組む。
S230：S229 の写し。転入＝手：その手に子0 を生まれたての新しい頭（種＋1000003）に入れ替える。
S229：S228 の写し。話し方＝'耳'：話し手は、自分が聞き手として合図 c を聞いたら場所 L を選ぶ値（v4 の手の点＝λ·Q＋kf·(食べ予測−平均)、聞き手の入力で読む）が一番高い c を出す（乱数［種,42］で 0.1 はでたらめ）。
S228：S227 の写し。組み方＝'毎回'（S227）／'固定'（はじめの組をずっと・役も固定）／'固定・役交代'（組は固定・奇数の手で役を入れ替え）。組の乱数は毎手引く（毎回と乱数の流れをそろえる）。
S227 言葉が要る世界（言葉の章の最初）：知っている子と動ける子を分ける。
赤ちゃん8人。毎手、乱数［種,40］で 4組（話し手・聞き手）に組み替える。各組に ご飯の場所 L（4か所、乱数［種,41］）。
話し手：入力に 場所 L（4つの印）と「話し手」の印。手（4つ）がそのまま合図になる。自分では食べない。
聞き手：入力に 合図（4つの印）と「聞き手」の印（見える＝True なら 場所 L も）。手（4つ）が選んだ場所。当たれば食べる（空腹 −一食）。
話し手は共感で、聞き手の苦しさ（h²）が減った分 を 共感量 に（頭が kE 倍して前の手の報酬に足す）。
入力は 場所4＋合図4＋役1＝9次元（頭の感覚に入る）。"""
import hashlib, numpy as np
人数 = 8; 次元 = 9
def 一生(種, 包, W, 寿命=16000, 見える=False, 頭='獲得型', 組み方='毎回', 話し方='ふつう', 点=None, 転入=None, 群れ=None, 入れ替え=None, 耳組=(), 選び替え=None):
    W.見た目次元 = 次元
    子 = [包(種, i, 頭) for i in range(人数)]
    群乱 = np.random.default_rng([種, 43]); 耳乱 = np.random.default_rng([種, 42]); 組乱 = np.random.default_rng([種, 40]); 場乱 = np.random.default_rng([種, 41])
    話列 = np.zeros((寿命, 4), dtype=np.int8); 聞列 = np.zeros((寿命, 4), dtype=np.int8); 合列 = np.zeros((寿命, 4), dtype=np.int8); 場列 = np.zeros((寿命, 4), dtype=np.int8); 当列 = np.zeros((寿命, 4), dtype=bool)
    h列 = np.zeros((寿命 // 100, 人数)); sha = hashlib.sha256()
    生まれ = np.zeros(人数); 替数 = 0   # S232
    for k in 耳組: 子[k].耳 = True   # S233
    空和 = np.zeros(人数); 耳数列 = []; 選数 = 0
    for t in range(寿命):
        if 転入 is not None and t == 転入: 子[0] = 包(種 + 1000003, 0, 頭)   # S230
        if 入れ替え is not None and t >= 入れ替え[0] and (t - 入れ替え[0]) % 入れ替え[1] == 0:   # S232
            k = int(np.argmin(生まれ)); 替数 += 1; 子[k] = 包(種 + 3000003 + 替数, k, 頭); 生まれ[k] = t
        並 = 組乱.permutation(人数); L = 場乱.integers(4, size=4)
        if 群れ is not None and 群乱.random() >= 群れ: 並 = np.concatenate([群乱.permutation(4), 4 + 群乱.permutation(4)])   # S231
        if 組み方 != '毎回':   # S228
            if t == 0: 並0 = 並.copy()
            並 = 並0.copy()
            if 組み方 == '固定・役交代' and t % 2 == 1: 並 = 並.reshape(4, 2)[:, ::-1].ravel()
        for p in range(4):
            sp, li = int(並[2 * p]), int(並[2 * p + 1]); 話列[t, p], 聞列[t, p], 場列[t, p] = sp, li, L[p]
            x = np.zeros(次元); x[L[p]] = 1.0; x[8] = 1.0
            φs = 子[sp].感覚(x); a_s, q_s, _ = 子[sp].選ぶ(φs)
            if 話し方 == '耳' or (話し方 == '型' and getattr(子[sp], '耳', False)):   # S229・S233
                if 耳乱.random() < 0.1: a_s = int(耳乱.integers(4))
                else:
                    v = []
                    for c in range(4):
                        z = np.zeros(次元); z[4 + c] = 1.0; v.append(点(子[sp], 子[sp].感覚(z))[L[p]])
                    a_s = int(np.argmax(v))
            合列[t, p] = a_s
            y = np.zeros(次元); y[4 + a_s] = 1.0
            if 見える: y[L[p]] = 1.0
            φl = 子[li].感覚(y); a_l, q_l, _ = 子[li].選ぶ(φl); 当 = (a_l == L[p]); 当列[t, p] = 当
            前h = 子[li].h
            子[sp].受ける(φs, a_s, q_s, 0.0, False, 0.0)
            子[li].受ける(φl, a_l, q_l, 0.0, bool(当), 0.0)
            子[sp].共感量 = 前h ** 2 - 子[li].h ** 2 if 当 else 0.0
        if t % 100 == 0: h列[t // 100] = [c.h for c in 子]
        if 選び替え is not None:   # S233
            空和 += np.array([c.h for c in 子])
            if t >= 選び替え[0] and (t + 1) % 選び替え[1] == 0:
                悪, 良 = int(np.argmin(-空和)), int(np.argmin(空和)); 型 = bool(getattr(子[良], '耳', False)); 選数 += 1
                子[悪] = 包(種 + 2000003 + 選数, 悪, 頭); 子[悪].耳 = 型
            if (t + 1) % 選び替え[1] == 0: 空和 = np.zeros(人数); 耳数列.append(sum(bool(getattr(c, '耳', False)) for c in 子))
        sha.update(合列[t].tobytes()); sha.update(当列[t].tobytes())
    return dict(耳数列=耳数列, 話列=話列, 聞列=聞列, 合列=合列, 場列=場列, 当列=当列, h列=h列, sha256=sha.hexdigest())
