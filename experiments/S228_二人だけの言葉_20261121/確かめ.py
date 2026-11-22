import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S227_言葉が要る世界_20261121', "数え.C.一生(900, 2000)['sha256']"); b = run('S228_二人だけの言葉_20261121', "数え.C.一生(900, 2000)['sha256']"); c = run('S228_二人だけの言葉_20261121', "数え.C.一生(900, 2000, 組み方='固定')['sha256']"); d = run('S228_二人だけの言葉_20261121', "数え.C.一生(900, 2000, 組み方='固定・役交代')['sha256']")
print('毎回＝S227', a == b != 'ERR', a[:12]); print('3つが違う', len({b, c, d}) == 3 and 'ERR' not in (c, d))
for k in ['毎回', '固定', '固定・役交代']: print(k, run('S228_二人だけの言葉_20261121', f"数え.測る(900, '{k}', 寿命=4000)[:3]"))
