import sys, importlib.util
from multiprocessing import Pool
P = '../'
def 並(job):
    w, 名, s = job; sp = importlib.util.spec_from_file_location('S172一覧', P + 'S172_v7は見本なしでv4と同じか_20261120/一覧.py'); G = importlib.util.module_from_spec(sp); sp.loader.exec_module(G)
    return G.並び((w, G.構成[名], s))
if __name__ == '__main__':
    W = ['48', '64', '116', '122', '125', '150', '164']; S = [900, 901, 902]; jobs = [(w, 名, s) for 名 in ['v4', 'v7', '元'] for w in W for s in S]
    with Pool(8, maxtasksperchild=1) as p: r = dict(zip(jobs, p.map(並, jobs, chunksize=1)))
    同 = {w: sum(r[(w, 'v4', s)] == r[(w, 'v7', s)] for s in S) for w in W}; 違 = {w: sum(r[(w, 'v4', s)] != r[(w, '元', s)] for s in S) for w in W}
    print('v7＝v4（各3組）:', 同, ' 計', sum(同.values()), '/21'); print('対照 v4≠元（各3組）:', 違, ' 計', sum(違.values()), '/21')
