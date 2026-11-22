import sys, numpy as np
sys.path.insert(0, '../S244_決まりなしの言葉の習得_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何 = job
    if 何 == '転入': return (数え.転入(s)[0], 0.0)
    if 何 == '群れ': return tuple(数え.群れ(s)[:2])
    return tuple(数え.継承(s)[:2])
if __name__ == '__main__':
    J = [(s, 何) for 何 in ['転入', '群れ', '継承'] for s in range(900, 910)]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, J, chunksize=1)
    R = {}
    for (s, 何), v in zip(J, r): R.setdefault(何, []).append(v)
    a, b, c = (np.array(R[k]) for k in ['転入', '群れ', '継承'])
    print('(a) 新入りの一致', a[:, 0].tolist(), f'>0.5 {int((a[:,0] > 0.5).sum())}/10')
    print('(b) 群れの中', np.round(b[:, 0], 2).tolist(), 'どうし', np.round(b[:, 1], 2).tolist(), f'どうし<中 {int((b[:,1] < b[:,0]).sum())}/10')
    print('(c) 最初の言葉との一致', c[:, 0].tolist(), '最後の当たり 中央値', round(float(np.median(c[:, 1])), 3), f'一致1.0 {int((c[:,0] == 1.0).sum())}/10')
