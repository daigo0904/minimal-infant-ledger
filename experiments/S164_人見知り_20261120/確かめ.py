import sys, importlib.util
sys.path.insert(0, '../S164_人見知り_20261120')
from 共 import *
a = 一生(900, '見る', 'v4', 1500); b = 一生(900, '見る', 'v4', 1500, 知らない=(700, 0.3))
S = importlib.util.spec_from_file_location('S151選び', '../S151_損も見る食べ予測_20261120/選び.py'); G = importlib.util.module_from_spec(S); S.loader.exec_module(G)
print('知らないなし＝S151 の v3損も:', a['sha256'] == G.C.一生(900, '見る', 'v3損も', 1500)['sha256'], ' 知らないで手が変わる:', a['sha256'] != b['sha256'])
import numpy as np; 相 = b['相手列']; print('知らない大人の割合 700以降:', round(float((相[700:] == 9).mean()), 3), ' 700前:', int((相[:700] == 9).sum()), ' 養育者:', round(float((相[700:] == 0).mean()), 3))
print(人見(b, 700, 1500))
