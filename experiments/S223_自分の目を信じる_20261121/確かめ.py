import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S222_狙い撃ちの悪口_20261121', "数え.一生(900, (0,1,2,3), 7, 0, 寿命=3000)['sha256']"); b = run('S223_自分の目を信じる_20261121', "数え.一生(900, (0,1,2,3), 7, 0, 寿命=3000)['sha256']"); c = run('S223_自分の目を信じる_20261121', "数え.一生(900, (0,1,2,3), 7, 0, 寿命=3000, ふるい=0.2)['sha256']")
print('ふるいなし＝S222', a == b != 'ERR', a[:12]); print('ふるいで変わる', c != b and c != 'ERR', c[:12])
