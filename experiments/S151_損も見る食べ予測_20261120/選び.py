import sys, numpy as np, importlib.util
sys.path.insert(0, '../S150_見に行くことが割に合う世界_20261120')
from multiprocessing import Pool
import 共 as C
_sp = importlib.util.spec_from_file_location('S151v2', '../S151_損も見る食べ予測_20261120/v2.py'); V = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(V)
C.V = V; C.包 = V.に(C.元換算, C.W, C.B)
C.構成['v3損も'] = dict(C.構成['v3'], 損も=True); C.構成['v3損も kf10'] = dict(C.構成['v3'], 損も=True, kf=10.0)
def one(job): s, 名 = job; o = C.一生(s, '見る', 名); return C.数える(o, 0, 1000) + C.数える(o, 7000, 8000)
if __name__ == '__main__':
    if sys.argv[1:] == ['確かめ']:
        A = L = None
        _s2 = importlib.util.spec_from_file_location('S150共元', '../S150_見に行くことが割に合う世界_20261120/共.py'); X = importlib.util.module_from_spec(_s2); _s2.loader.exec_module(X)
        print('損もなしの v3 は S150 と同じ sha:', C.一生(900, '見る', 'v3', 1500)['sha256'] == X.一生(900, '見る', 'v3', 1500)['sha256']); sys.exit()
    with Pool(8) as p:
        for 名 in ['v3', 'v3損も', 'v3損も kf10']:
            r = np.array(p.map(one, [(s, 名) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'{名}: 分からない時に顔を見る − 分かる時 初め {m[0]:+.3f} 終わり {m[5]:+.3f}（>0 {int((r[:,5] > 0).sum())}/10）（見る 無 {m[6]:.3f} 有 {m[7]:.3f}） | 見えた表情に従う {m[8]:+.3f} | 食べ {m[9]:.4f}')
