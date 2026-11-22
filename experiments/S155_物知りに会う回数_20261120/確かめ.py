import sys, importlib.util, numpy as np
sys.path.insert(0, '../S155_物知りに会う回数_20261120')
from 共 import 一生
P = '../'
a = 一生(900, '養育者', 'v4', 寿命=1500, 物知り=(1, 0.7))
b = 一生(900, '養育者', 'v4', 寿命=1500, 物知り=(1, 0.7), 物知り率=0.5)
for o, n in [(a, 'そのまま'), (b, '0.5')]:
    相 = o['相手列']; m = np.arange(8) != 1; 仲 = 相[:, m][相[:, m] > 0]; print(n, '仲間番で物知りの割合', round(float((仲 == 2).mean()), 3), '養育者の割合', round(float((相 == 0).mean()), 3))
print('sha そのまま≠0.5:', a['sha256'] != b['sha256'])
print('sha:', a['sha256'])
