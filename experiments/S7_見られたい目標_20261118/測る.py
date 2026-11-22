import sys, json, numpy as np
import 世界 as W
W.感覚数 = 256; W.見た目雑音 = 0.3
def P養(o, lo, hi):
    A, 相, b = o['行動列'], o['相手列'], o['一番']
    return float(np.mean([(A[lo:hi, i][相[lo:hi, i] == 0] == b).mean() for i in range(8)]))
def 一つ(s, h):
    out = {}
    for 試 in [None, '欠乏', '飽和']:
        o = W.一生(s, '依存', h, 寿命=8700, 離乳=8000, 試し=試)
        out[str(試)] = dict(戻って=P養(o, 8500, 8700), 前=P養(o, 7500, 8000), sha=o['sha256'])
    return out
if __name__ == '__main__':
    for s in [int(x) for x in sys.argv[2:]]:
        for h in sys.argv[1].split(','):
            r = 一つ(s, h)
            print(s, h, {k: round(v['戻って'], 3) for k, v in r.items()}, '前', round(r['None']['前'], 3), '同じ前半', r['None']['前'] == r['欠乏']['前'], flush=True)
