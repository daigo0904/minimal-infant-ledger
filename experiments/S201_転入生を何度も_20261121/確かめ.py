import sys
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S201_転入生を何度も_20261121'); import 数え; return 数え.測る(900, 5.0, 転入=x, 寿命=1500)
def 旧(_):
    sys.path.insert(0, '../S199_困っている子にも寄る_20261121'); import 数え; return 数え.測る(900, 5.0, 寿命=1500)
def 旧200(_):
    sys.path.insert(0, '../S200_転入生_20261121'); import 数え; return 数え.測る(900, 5.0, 転入=700, 寿命=1500)
def 新200(_):
    sys.path.insert(0, '../S201_転入生を何度も_20261121'); import 共; return 共.一生(900, 'v4', 1500, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.3, 困寄る=5.0, 転入=700)['sha256']
if __name__ == '__main__':
    with Pool(4, maxtasksperchild=1) as p: a = p.map(新, [False])[0]; b = p.map(旧, [0])[0]; c = p.map(旧200, [0])[0]; d = p.map(新200, [0])[0]
    print('入れ替えなし＝S199:', a == b, ' 1人の転入（700）＝S200:', c == d)
