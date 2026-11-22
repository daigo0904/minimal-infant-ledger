"""調整用の種 900〜909：S100 の損の世界（多数・kM5）で、元／v3 の部品つき、しきたり 決まった手／でたらめ。代替わり後 8500〜 のしきたり。"""
import sys, numpy as np, importlib.util
from multiprocessing import Pool
P = '../'
sys.path.insert(0, P + 'S100_多数に合わせる_20261119')
def L(n, p):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = L('S100R', P + 'S100_多数に合わせる_20261119/走らせる.py'); 共 = sys.modules['共通']
V = L('S142v2', P + 'S142_空腹で切り替える_20261120/v2.py'); X = L('S145写すv3', P + 'S145_v3としきたり_20261120/写すv3.py')
元写す = 共.H.写す; 包 = X.作る(V, 共.H, 共.W, 共.B)
構成 = {'元': dict(), 'v3': dict(kf=3.0, kD=30.0, λ=0.2, kJ=5.0, 切替='J満')}
def 世(s, 名, 型, 寿命=10000):
    V.設定.update(kf=0.0, kD=0.0, λ=1.0, 窓=3, kf型='普通', kS=0.0, kJ=0.0, 切替=None); V.設定.update(構成[名]); 共.H.写す = 包
    try: return R.世(s, '流行り', True, 型, 寿命)
    finally: 共.H.写す = 元写す
def one(job):
    s, 名, 型 = job; o = 世(s, 名, 型); x = R.しきたりの手(s); return float((o['行動列'][8500:] == x).mean()), float(o['食列'][8500:].mean())
if __name__ == '__main__':
    if sys.argv[1:] == ['確かめ']:
        a = R.世(900, '流行り', True, '決まった手', 3000)['sha256']; b = 世(900, '元', '決まった手', 3000)['sha256']; c = 世(900, 'v3', '決まった手', 3000)['sha256']
        print('v3（全部0）は S100 と同じ:', a == b, ' v3 で手が変わる:', b != c); sys.exit()
    with Pool(8) as p:
        for 名 in 構成:
            r = {型: np.array(p.map(one, [(s, 名, 型) for s in range(900, 910)])) for 型 in ['決まった手', 'でたらめ']}
            効 = r['決まった手'][:, 0] - r['でたらめ'][:, 0]
            print(f'{名}: しきたり 決まった手 {np.median(r["決まった手"][:,0]):.3f} でたらめ {np.median(r["でたらめ"][:,0]):.3f} 効き>0 {int((効 > 0).sum())}/10  食べ {np.median(r["決まった手"][:,1]):.4f}')
