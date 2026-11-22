import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S217_噂_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.01)['sha256']"); b = run('S218_なぜ得が増えないか_20261121', "数え.一生(900, 5.0, '見た', (0,1,2,3), 3000, 0.01)['sha256']")
c = run('S217_噂_20261121', "数え.測る(900, ρ=5.0, 私的='見た', 噂=0.01, 寿命=3000)[0]"); d = run('S218_なぜ得が増えないか_20261121', "round(数え.測る(900, 噂=0.01, 寿命=3000)[-2], 12)")
print('sha＝S217', a == b != 'ERR', a[:12]); print('得＝S217', c, d, abs(float(c) - float(d)) < 1e-9 if 'ERR' not in (c, d) else False)
