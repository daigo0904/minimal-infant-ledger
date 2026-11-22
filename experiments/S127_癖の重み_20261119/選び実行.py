import importlib.util, numpy as np
from multiprocessing import Pool
sp = importlib.util.spec_from_file_location('S127選び', '../S127_癖の重み_20261119/選び.py'); S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
def one(job): return S.one(job)
if __name__ == '__main__':
    with Pool(8) as p:
        for λ in [1.0, 0.5, 0.2]:
            r = np.array(p.map(one, [(s, λ) for s in range(900, 910)])); m = np.median(r, 0)
            print(f'λ={λ}: S125 指す 褒める 初め {m[0]:.3f}→終わり {m[1]:.3f}（育つ {int((r[:,1] > r[:,0]).sum())}/10）・褒めない {m[2]:.3f} 食べ {m[3]:.4f} | S64 増え {m[4]:+.3f}（>0 {int((r[:,4] > 0).sum())}/10）P養 {m[5]:.3f} | S48 本物 {m[6]:.3f}')
