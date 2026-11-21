import sys, subprocess
def sha(d, args): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print(数え.測る(900, 1.0, 寿命=3000, {args}))"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = sha('S211_評判で寄る_20261121', 'β=0.0, ρ=5.0'); b = sha('S212_見られている時だけ_20261121', 'β=0.0, ρ=5.0'); c = sha('S212_見られている時だけ_20261121', 'β=0.0, ρ=5.0, 見評=True'); d = sha('S212_見られている時だけ_20261121', 'β=0.0, ρ=5.0, 観=True')
print('口なし＝S211', a == b, a[:12]); print('見られ評判で変わる', c != b, c[:12]); print('観客入力で変わる', d != b and d != 'ERR', d[:12])
