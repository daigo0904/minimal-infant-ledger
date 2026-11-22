import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S230_言葉の習得_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']"); b = run('S231_方言_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']"); c = run('S231_方言_20261121', "数え.C.一生(900, 2000, 話し方='耳', 群れ=0.02)['sha256']")
print('群れなし＝S230', a == b != 'ERR', a[:12]); print('群れで変わる', c != b and c != 'ERR', c[:12])
for m in [0.02, 0.5]: print(m, run('S231_方言_20261121', f"数え.測る(900, {m}, 寿命=6000)[:4]"))
