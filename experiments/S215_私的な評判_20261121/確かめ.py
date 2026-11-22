import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S211_評判で寄る_20261121', "数え.測る(900, 1.0, β=0.0, ρ=5.0, 寿命=3000)"); b = run('S215_私的な評判_20261121', "数え.C.一生(900, 'v4', 3000, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 親切=3.0, 親切組=(0,1,2,3), 選び替え=(2000,250), 評判=5.0)['sha256']")
c = run('S215_私的な評判_20261121', "数え.一生(900, 5.0, True, (0,1,2,3), 3000)['sha256']"); d = run('S215_私的な評判_20261121', "数え.一生(900, 5.0, False, (0,1,2,3), 3000)['sha256']")
print('口なし＝S211', a == b and a != 'ERR', a[:12], b[:12]); print('私的で変わる', c != d and 'ERR' not in (c, d), c[:12], d[:12])
