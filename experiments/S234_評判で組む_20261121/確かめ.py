import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S233_耳の型は増えるか_20261121', "数え.増える(900, 寿命=3000)"); b = run('S234_評判で組む_20261121', "数え.増える(900, 0.0, 寿命=3000)"); c = run('S234_評判で組む_20261121', "数え.増える(900, 5.0, 寿命=3000)")
print('ρ0＝S233', a == b != 'ERR', a[-16:], b[-16:]); print('ρで変わる', c != b and c != 'ERR')
print('安い試し 得 ρ5', run('S234_評判で組む_20261121', "数え.得(900, 5.0, 寿命=4000)[:2]"), 'ρ0', run('S234_評判で組む_20261121', "数え.得(900, 0.0, 寿命=4000)[:2]"))
