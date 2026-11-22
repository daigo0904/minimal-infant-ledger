import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S223_自分の目を信じる_20261121', "数え.一生(900, (0,1,2,3), None, None, 寿命=3000, ふるい=0.05)['sha256']"); b = run('S224_頑固さの代価_20261121', "数え.一生(900, (0,1,2,3), 0.05, 0.05, None, 3000)['sha256']"); c = run('S224_頑固さの代価_20261121', "数え.一生(900, (0,1,2,3), 0.05, 0.05, (1500, 7), 3000)['sha256']")
print('変身なし＝S223', a == b != 'ERR', a[:12]); print('変身で変わる', c != b and c != 'ERR', c[:12])
d = run('S224_頑固さの代価_20261121', "数え.測る(900, 寿命=4000, 変わり目=2000)[:3]"); print('安い試し（4000手・2000で変身）', d)
