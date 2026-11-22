import sys, importlib.util
from multiprocessing import Pool
def 新(x):
    sys.path.insert(0, '../S210_親切どうしが寄り合う_20261121'); import 数え; return 数え.測る(900, 1.0, β=0.3, 寿命=3000, 選=(1000, 250), δ=x)
def 旧(_):
    sp = importlib.util.spec_from_file_location('S205共', '../S205_親切は広がるか_20261121/共.py'); C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
    return C.一生(900, 'v4', 3000, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.3, 困寄る=0.0, 親切=3.0, 親切組=(0, 1, 2, 3), 選び替え=(1000, 250))['sha256']
if __name__ == '__main__':
    with Pool(3, maxtasksperchild=1) as p: a, b = p.map(新, [0.0, 2.0], chunksize=1); c = p.map(旧, [0])[0]
    print('δ0＝S205/S209 の作り:', a == c, ' δ2 で変わる:', a != b)
