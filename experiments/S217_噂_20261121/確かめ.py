import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S216_受けたか見たか_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000)['sha256']"); b = run('S217_噂_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000)['sha256']"); c = run('S217_噂_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.05)['sha256']")
print('噂なし＝S216', a == b != 'ERR', a[:12], b[:12]); print('噂で変わる', c != b and c != 'ERR', c[:12])
