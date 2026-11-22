import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
a = run('S232_文化の継承_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']"); b = run('S233_耳の型は増えるか_20261121', "数え.C.一生(900, 2000, 話し方='耳')['sha256']")
c = run('S233_耳の型は増えるか_20261121', "数え.C.一生(900, 2000, 話し方='型', 耳組=tuple(range(8)))['sha256']")
print('口なし＝S232', a == b != 'ERR', a[:12]); print('全員耳の型＝耳で話す', c == b, c[:12])
print('安い試し 増える', run('S233_耳の型は増えるか_20261121', "数え.C.一生(900, 4000, 50.0, False, '毎回', '型', None, None, None, (0,1,2,3), (1000, 250))['耳数列']"))
print('安い試し 得', run('S233_耳の型は増えるか_20261121', "数え.得(900, 寿命=4000)[0]"))
