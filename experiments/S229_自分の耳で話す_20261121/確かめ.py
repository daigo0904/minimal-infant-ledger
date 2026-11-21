import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S228_二人だけの言葉_20261121', "数え.C.一生(900, 2000)['sha256']"); b = run('S229_自分の耳で話す_20261121', "数え.C.一生(900, 2000)['sha256']"); c = run('S229_自分の耳で話す_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']")
print('ふつう＝S228', a == b != 'ERR', a[:12]); print('耳で変わる', c != b and c != 'ERR', c[:12])
for k in ['ふつう', '耳']: print(k, run('S229_自分の耳で話す_20261121', f"数え.測る(900, '{k}', 寿命=4000)[:4]"))
