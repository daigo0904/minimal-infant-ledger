import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S229_自分の耳で話す_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']"); b = run('S230_言葉の習得_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']"); c = run('S230_言葉の習得_20261121', "数え.C.一生(900, 2000, 話し方='耳', 転入=1000)['sha256']")
print('転入なし＝S229', a == b != 'ERR', a[:12]); print('転入で変わる', c != b and c != 'ERR', c[:12])
for k in ['耳', 'ふつう']: print(k, run('S230_言葉の習得_20261121', f"数え.測る(900, '{k}', 寿命=8000, 転入=4000)[:3]"))
