import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S231_方言_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']"); b = run('S232_文化の継承_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']"); c = run('S232_文化の継承_20261121', "数え.C.一生(900, 2000, 話し方='耳', 入れ替え=(1000, 250))['sha256']")
print('入れ替えなし＝S231', a == b != 'ERR', a[:12]); print('入れ替えで変わる', c != b and c != 'ERR', c[:12])
for k in ['耳', 'ふつう']: print(k, run('S232_文化の継承_20261121', f"数え.測る(900, '{k}', 寿命=8000, 入れ替え=(2000, 250))[:3]"))
