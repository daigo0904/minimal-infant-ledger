import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S225_公平_20261121', "数え.一生(900, True, 3000)['sha256']"); b = run('S226_公平の気持ち_20261121', "数え.一生(900, 0.0, True, 3000)['sha256']"); c = run('S226_公平の気持ち_20261121', "数え.一生(900, 5.0, True, 3000)['sha256']")
print('kQ0＝S225', a == b != 'ERR', a[:12]); print('kQで変わる', c != b and c != 'ERR', c[:12]); print('安い試し kQ5', run('S226_公平の気持ち_20261121', "数え.測る(900, 5.0, 4000)[:4]"), 'kQ0', run('S226_公平の気持ち_20261121', "数え.測る(900, 0.0, 4000)[:4]"))
