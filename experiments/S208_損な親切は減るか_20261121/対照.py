import sys, numpy as np
sys.path.insert(0, '../S208_損な親切は減るか_20261121')
from multiprocessing import Pool
def one(job):
    import 数え; s, k = job; return 数え.測る(s, 1.0, 親切=k)[:2]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p: r = np.array(p.map(one, [(s, 1.0) for s in range(900, 910)], chunksize=1))
    print('対照（印だけ・親切1倍）kG1: 終わりの印の数', np.round(r[:,0], 1).tolist(), ' 中ほど', np.round(r[:,1], 1).tolist())
