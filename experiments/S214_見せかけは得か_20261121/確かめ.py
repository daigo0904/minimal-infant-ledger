import sys, subprocess
a = subprocess.run([sys.executable, '-c', "import sys; sys.path.insert(0,'../S213_見せかけの型_20261121'); import 数え; print(数え.測る(900, 見評=True, 寿命=3000, 選=None))"], capture_output=True, text=True).stdout.strip() or 'ERR'
b = subprocess.run([sys.executable, '-c', "import sys; sys.path.insert(0,'../S214_見せかけは得か_20261121'); import 数え; print(数え.一生(900, True, (2, 3), 3000)['sha256'])"], capture_output=True, text=True).stdout.strip() or 'ERR'
print('S213 の選び替えなし＝S214', a == b and a != 'ERR', a[:12], b[:12])
