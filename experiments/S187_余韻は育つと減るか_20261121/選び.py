import sys, numpy as np
sys.path.insert(0, '../S185_見られ分けの余韻_20261121')
from multiprocessing import Pool
import 共
def one(job): s, 名 = job; o = 共.一生(s, 名, 記憶=0.5); return [共.余韻(o, lo, lo + 1000) for lo in range(1000, 8000, 1000)]
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for 名 in ['元', 'v4']:
            r = np.array(p.map(one, [(s, 名) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'{名}: 余韻 ' + ' '.join(f'{v:+.3f}' for v in m[:, 0]) + ' ／ 見られ分け ' + ' '.join(f'{v:+.2f}' for v in m[:, 3]), flush=True)
            print(f'   終わり>初め {int((r[:, 6, 0] > r[:, 0, 0]).sum())}/10  山（最大が中ほど 2000〜6000）{int(np.isin(r[:, :, 0].argmax(1), [1, 2, 3, 4, 5]).sum())}/10', flush=True)
