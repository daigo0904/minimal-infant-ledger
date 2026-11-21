import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S219_嘘つきの噂_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.05, 7)['sha256']"); b = run('S220_嘘を見抜く_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.05, 7)['sha256']"); c = run('S220_嘘を見抜く_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.05, 7, True)['sha256']")
print('信用なし＝S219', a == b != 'ERR', a[:12]); print('信用で変わる', c != b and c != 'ERR', c[:12])
