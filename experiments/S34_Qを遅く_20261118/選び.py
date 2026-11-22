import numpy as np
from multiprocessing import Pool
import 頭 as H
if __name__ == '__main__':
    print('0.02≠0.05:', H.一生(999, 0.02, 600)['sha256'] != H.一生(999, 0.05, 600)['sha256'])
    L = [0.01, 0.02, 0.03, 0.05]
    with Pool(8) as p: r = p.map(H.one, [(s, lr) for lr in L for s in range(900, 910)])
    for lr in L:
        x = [y for y in r if y[1] == lr]
        print(lr, '初め差', round(np.median([y[2][2] for y in x]), 3), '育 P養/P他/差', [round(float(np.median([y[3][j] for y in x])), 3) for j in range(3)], '空腹', round(np.median([y[4] for y in x]), 3), '育ち', sum(y[2][2] <= y[3][2] / 2 for y in x))
