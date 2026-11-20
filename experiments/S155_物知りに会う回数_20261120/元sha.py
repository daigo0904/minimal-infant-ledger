import sys
sys.path.insert(0, '../S153_表情の信頼性_20261120')
from 共 import 一生
print('sha:', 一生(900, '養育者', 'v4', 寿命=1500, 物知り=(1, 0.7))['sha256'])
