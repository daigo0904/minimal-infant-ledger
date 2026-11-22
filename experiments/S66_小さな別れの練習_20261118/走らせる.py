import sys, json, numpy as np, importlib.util
from multiprocessing import Pool
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
H = L('S65頭', '../S65_見られ方のホメオスタシス_20261118/頭.py')
B, W, M = H.B, H.W, H.M
N = L('S66世界', '../S66_小さな別れの練習_20261118/世界.py'); N.感覚数 = 256; N.見た目雑音 = 0.3
H.設定.update(目標=0.3, k=1.0)
世界 = {'なし': None, '欠乏': '欠乏', '練習だけ': '練習だけ', '繰り返し欠乏': '繰り返し欠乏'}
def 一生(s, 頭, 試, 寿命=8000):
    W.学び率 = 0.01; B.v時定数 = 5000.0; N.赤ちゃん = H.恒常 if 頭 == 'あり' else B.換算
    try: return N.一生(s, '依存', '獲得型', 寿命=寿命, 離乳=寿命, 給餌の形='その手だけ', 試し=世界[試])
    finally: W.学び率 = 0.05; B.v時定数 = 1000.0
def one(job):
    s, 頭, 試 = job; o = 一生(s, 頭, 試); return (s, 頭, 試, M.P養(o, 7500, 7700))
if __name__ == '__main__':
    if sys.argv[1] == '確かめ':
        o = 一生(16799, 'あり', '繰り返し欠乏'); 相 = o['相手列']
        print('練習の別れで養育者が見る手:', [int((相[a:a + 200] == 0).sum()) for a in range(1000, 7000, 1000)], ' 本番:', int((相[7000:7500] == 0).sum()), ' 普段(800〜1000):', int((相[800:1000] == 0).sum()))
        a = 一生(16799, 'あり', '練習だけ'); print('練習だけ と 繰り返し欠乏 は 7000 まで同じ:', bool((a['行動列'][:7000] == o['行動列'][:7000]).all()))
        b = 一生(16799, 'なし', '欠乏'); c = M.一生(16799, '欠乏'); print('なし×欠乏 ＝ S64:', b['sha256'] == c['sha256'])
        H.設定.update(目標=0.3, k=1.0); print('設定:', H.設定); sys.exit()
    段 = sys.argv[1]; S = range(16600, 16630) if 段 == '本' else range(16700, 16730)
    with Pool(8) as p: r = p.map(one, [(s, h, w) for h in ['あり', 'なし'] for w in 世界 for s in S])
    d = {(s, h, w): x for s, h, w, x in r}
    増 = lambda s, h, 練: d[(s, h, '繰り返し欠乏')] - d[(s, h, '練習だけ')] if 練 else d[(s, h, '欠乏')] - d[(s, h, 'なし')]
    res = dict(H1_練習ありで戻って増える=int(sum(増(s, 'あり', True) > 0 for s in S)), H2_ホメオスタシスの分=int(sum(増(s, 'あり', True) > 増(s, 'なし', True) for s in S)), H3_練習の分=int(sum(増(s, 'あり', True) > 増(s, 'あり', False) for s in S)))
    res['判定'] = {k: v >= 20 for k, v in res.items()}
    res['増え_中央値'] = {f'{h}_{"練習あり" if t else "練習なし"}': round(float(np.median([増(s, h, t) for s in S])), 3) for h in ['あり', 'なし'] for t in [True, False]}
    res['P養_中央値'] = {f'{h}_{w}': round(float(np.median([d[(s, h, w)] for s in S])), 3) for h in ['あり', 'なし'] for w in 世界}
    print(json.dumps(res, ensure_ascii=False)); json.dump(dict(結果=res, 行=r), open(f'結果_{段}.json', 'x'), ensure_ascii=False, indent=1)
