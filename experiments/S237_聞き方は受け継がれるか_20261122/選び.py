import sys, numpy as np
sys.path.insert(0, '../S237_聞き方は受け継がれるか_20261122')
from multiprocessing import Pool
def one(job):
    import 数え; s, 何 = job; return (数え.増える(s)[0], 0.0, 0.0) if 何 == '増' else tuple(数え.得(s)[:3])
if __name__ == '__main__':
    J = [(s, 何) for 何 in ['増', '得'] for s in range(900, 910)]
    with Pool(8, maxtasksperchild=1) as p: r = p.map(one, J, chunksize=1)
    R = {}
    for (s, 何), v in zip(J, r): R.setdefault(何, []).append(v)
    a, g = np.array(R['増']), np.array(R['得'])
    print('終わりの分けて聞く子', np.round(a[:, 0], 2).tolist(), '中央値', np.median(a[:, 0]))
    print('空腹差 まとめて−分けて', np.round(g[:, 0], 3).tolist(), '中央値', round(float(np.median(g[:, 0])), 4), '・当たり 分けて', round(float(np.median(g[:, 1])), 3), 'まとめて', round(float(np.median(g[:, 2])), 3))
    print(f'分けて>4 {int((a[:,0] > 4).sum())}/10・分けてが得 {int((g[:,0] > 0).sum())}/10・聞き手の当たり 分けて>まとめて {int((g[:,1] > g[:,2]).sum())}/10')
