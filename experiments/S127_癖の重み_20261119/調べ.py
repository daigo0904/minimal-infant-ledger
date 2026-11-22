import importlib.util
from multiprocessing import Pool
sp = importlib.util.spec_from_file_location('S127選び', '../S127_癖の重み_20261119/選び.py'); S = importlib.util.module_from_spec(sp); sp.loader.exec_module(S)
def f(λ):
    S.G.設定['λ'] = λ; return λ, S.R64.B.換算.__name__, getattr(S.R64.B.換算, '_λ', None), S.R64.一生(900, 'なし', 寿命=1500)['sha256'][:12]
if __name__ == '__main__':
    with Pool(2) as p: print(p.map(f, [1.0, 0.2]))
