import sys, numpy as np
sys.path.insert(0, '../S177_14か月から18か月_20261120')
from multiprocessing import Pool
from 数え import 測る
def one(job): return np.array(測る(*job)[0])
if __name__ == '__main__':
    with Pool(8, maxtasksperchild=1) as p:
        for x in [0.05, 0.1]:
            r = np.array(p.map(one, [(s, 'v4', x) for s in range(900, 910)], chunksize=1)); m = np.median(r, 0)
            print(f'v4 自分{x}: B の前 B好き−自分好き ' + ' '.join(f'{v:+.2f}' for v in m[:, 0]) + ' ／ 仲間の前の自分好き ' + ' '.join(f'{v:.2f}' for v in m[:, 1]), flush=True)
            print(f'   初め(0-1000) < 0: {int((r[:, 0, 0] < 0).sum())}/10  最小の区間が終わりより前: {int((r[:, :, 0].argmin(1) < 7).sum())}/10  終わり > 初め: {int((r[:, 7, 0] > r[:, 0, 0]).sum())}/10  自分好きが B好き−自分好き より先に上がる(1000-2000 で 仲間の前の自分好き>0.3): {int((r[:, 1, 1] > 0.3).sum())}/10')
