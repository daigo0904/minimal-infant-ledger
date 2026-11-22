"""S177：S176 の世界・頭を読むだけ。1000手ごとに ブロッコリー（B の前の B好き−自分好き、仲間の前の自分好き、A の前の A好き−自分好き）。"""
import sys, numpy as np
sys.path.insert(0, '../S176_本物のブロッコリー課題_20261120')
from 共 import 一生, ブロッコリー
def 測る(s, 名='v4', x=0.05):
    o = 一生(s, 名, 二人=0.5, 自分=x); return [ブロッコリー(o, lo, lo + 1000) for lo in range(0, 8000, 1000)], o['sha256']
