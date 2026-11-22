import sys, subprocess
def run(d, code): return subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0,'../{d}'); import 数え; print({code})"], capture_output=True, text=True).stdout.strip() or 'ERR'
code = "数え.C.一生(900, 'v4', 3000, なぐさめ=True, kE=50.0, 共感型='苦しさ', 泣き=0.01, 代価=0.03, 感謝=1.0, 寄る=0.0, 困寄る=0.0, 親切=1.0, 親切組=(), 選び替え=None)['sha256']"
a = run('S224_頑固さの代価_20261121', code); b = run('S225_公平_20261121', code); c = run('S225_公平_20261121', "数え.一生(900, True, 3000)['sha256']")
print('公平入力なし＝S224', a == b != 'ERR', a[:12]); print('公平入力で変わる', c != b and c != 'ERR', c[:12]); print('安い試し', run('S225_公平_20261121', "数え.測る(900, True, 4000)[:3]"))
