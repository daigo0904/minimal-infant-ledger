import sys, subprocess
def run(d, f, args): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({f}(900, 寿命=3000, {args}))"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S212_見られている時だけ_20261121', '数え.測る', 'β=0.0, ρ=5.0, 観=True, 見評=True'); b = run('S213_見せかけの型_20261121', '数え.測る', '見評=True, 見せ組=()'); c = run('S213_見せかけの型_20261121', '数え.測る', '見評=True')
print('見せ組なし＝S212', a == b and a != 'ERR', a[:12], b[:12]); print('見せ組で変わる', c != b and c != 'ERR', c[:12])
